"""Camera Management and Operational REST API endpoints."""

from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.app.camera.manager import camera_manager
from backend.app.camera.types import CameraTelemetryState
from backend.app.db.enums import CameraStatus
from backend.app.db.models.camera import Camera
from backend.app.db.session import get_db
from backend.app.schemas.camera import (
    CameraCreate,
    CameraResponse,
    CameraTelemetryResponse,
    CameraTestProbeResponse,
    CameraUpdate,
)

router = APIRouter(prefix="/cameras", tags=["Cameras"])


def _to_camera_response(camera: Camera) -> CameraResponse:
    """Format DB camera model to safe response, reflecting live worker status if active."""
    worker = camera_manager.get_worker(camera.id)
    current_status = camera.status.value if hasattr(camera.status, "value") else str(camera.status)
    if worker is not None:
        snapshot = worker.telemetry.get_snapshot()
        current_status = snapshot.runtime_status

    source_val = camera.source_type.value if hasattr(camera.source_type, "value") else str(camera.source_type)

    return CameraResponse(
        id=camera.id,
        name=camera.name,
        location=camera.location,
        source_type=source_val,
        device_index=camera.device_index,
        rtsp_url=camera.rtsp_url,
        credential_ref=camera.credential_ref,
        is_active=camera.is_active,
        status=current_status,
        target_fps=camera.target_fps,
        reconnect_delay=camera.reconnect_delay,
        created_at=camera.created_at,
        updated_at=camera.updated_at,
    )


@router.get("", response_model=List[CameraResponse], summary="List configured cameras")
def list_cameras(db: Session = Depends(get_db)) -> List[CameraResponse]:
    """Retrieve all configured camera sources with dynamic runtime status."""
    cameras = db.query(Camera).order_by(Camera.id.asc()).all()
    return [_to_camera_response(c) for c in cameras]


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED, summary="Create new camera")
def create_camera(payload: CameraCreate, db: Session = Depends(get_db)) -> CameraResponse:
    """Register a new camera source. Starts capture worker if is_active is true."""
    existing = db.query(Camera).filter(Camera.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "CAMERA_NAME_EXISTS", "message": f"Camera with name '{payload.name}' already exists."},
        )

    try:
        camera = Camera(
            name=payload.name,
            location=payload.location,
            source_type=payload.source_type,
            device_index=payload.device_index,
            rtsp_url=payload.rtsp_url,
            credential_ref=payload.credential_ref,
            target_fps=payload.target_fps,
            reconnect_delay=payload.reconnect_delay,
            is_active=True,
            status=CameraStatus.CONNECTING,
        )
        db.add(camera)
        db.commit()
        db.refresh(camera)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "VALIDATION_ERROR", "message": str(exc)},
        )

    # Launch background worker for the active camera
    if camera.is_active:
        camera_manager.start_camera(camera)

    return _to_camera_response(camera)


@router.get("/{camera_id}", response_model=CameraResponse, summary="Get camera by ID")
def get_camera(camera_id: int, db: Session = Depends(get_db)) -> CameraResponse:
    """Retrieve camera configuration and current runtime status."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )
    return _to_camera_response(camera)


@router.patch("/{camera_id}", response_model=CameraResponse, summary="Update camera configuration")
def update_camera(camera_id: int, payload: CameraUpdate, db: Session = Depends(get_db)) -> CameraResponse:
    """Update camera parameters. Re-initializes worker if stream settings change."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    if payload.name is not None and payload.name != camera.name:
        existing = db.query(Camera).filter(Camera.name == payload.name, Camera.id != camera_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_code": "CAMERA_NAME_EXISTS", "message": f"Camera with name '{payload.name}' already exists."},
            )

    update_data = payload.model_dump(exclude_unset=True)
    source_params_changed = any(
        k in update_data for k in ("source_type", "device_index", "rtsp_url", "credential_ref", "target_fps", "reconnect_delay")
    )

    try:
        for field, val in update_data.items():
            setattr(camera, field, val)
        camera.validate_consistency()
        db.commit()
        db.refresh(camera)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error_code": "VALIDATION_ERROR", "message": str(exc)},
        )

    # Handle worker restart or state changes
    if not camera.is_active:
        camera_manager.stop_camera(camera.id)
    elif source_params_changed:
        camera_manager.restart_camera(camera)
    else:
        # If camera was inactive and now marked active
        worker = camera_manager.get_worker(camera.id)
        if worker is None or not worker.is_running():
            camera_manager.start_camera(camera)

    return _to_camera_response(camera)


@router.delete(
    "/{camera_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete camera",
)
def delete_camera(camera_id: int, db: Session = Depends(get_db)) -> Response:
    """Stop active capture worker and delete camera record."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    # Ensure worker is stopped before deleting record
    camera_manager.stop_camera(camera_id)

    db.delete(camera)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{camera_id}/test", response_model=CameraTestProbeResponse, summary="Test camera connection")
def test_camera_connection(camera_id: int, db: Session = Depends(get_db)) -> CameraTestProbeResponse:
    """Perform a short-lived capture probe against configured camera without persisting frames."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    source_val = camera.source_type.value if hasattr(camera.source_type, "value") else str(camera.source_type)

    result = camera_manager.test_connection(
        source_type=source_val,
        device_index=camera.device_index,
        rtsp_url=camera.rtsp_url,
        credential_ref=camera.credential_ref,
        camera_id=camera.id,
    )

    return CameraTestProbeResponse(
        success=result.success,
        source_type=result.source_type,
        elapsed_ms=result.elapsed_ms,
        camera_id=result.camera_id,
        frame_width=result.frame_width,
        frame_height=result.frame_height,
        safe_error_code=result.safe_error_code,
        message=result.message,
    )


@router.post("/{camera_id}/start", response_model=CameraResponse, summary="Start camera capture")
def start_camera_endpoint(camera_id: int, db: Session = Depends(get_db)) -> CameraResponse:
    """Mark camera active and start its background capture worker."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    camera.is_active = True
    camera.status = CameraStatus.CONNECTING
    db.commit()
    db.refresh(camera)

    camera_manager.start_camera(camera)
    return _to_camera_response(camera)


@router.post("/{camera_id}/stop", response_model=CameraResponse, summary="Stop camera capture")
def stop_camera_endpoint(camera_id: int, db: Session = Depends(get_db)) -> CameraResponse:
    """Mark camera inactive, set status to DISABLED, and release capture worker."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    camera_manager.stop_camera(camera_id)

    camera.is_active = False
    camera.status = CameraStatus.DISABLED
    db.commit()
    db.refresh(camera)

    return _to_camera_response(camera)


@router.get("/{camera_id}/telemetry", response_model=CameraTelemetryResponse, summary="Get camera telemetry")
def get_camera_telemetry(camera_id: int, db: Session = Depends(get_db)) -> CameraTelemetryResponse:
    """Fetch high-frequency runtime telemetry (FPS, drop counters, latency) for a camera."""
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "CAMERA_NOT_FOUND", "message": f"Camera with ID {camera_id} not found."},
        )

    snapshot = camera_manager.get_telemetry(camera_id)
    source_val = camera.source_type.value if hasattr(camera.source_type, "value") else str(camera.source_type)

    if snapshot is None:
        status_val = camera.status.value if hasattr(camera.status, "value") else str(camera.status)
        snapshot = CameraTelemetryState(
            camera_id=camera.id,
            camera_name=camera.name,
            source_type=source_val,
            runtime_status=status_val,
            worker_running=False,
        )

    return CameraTelemetryResponse(
        camera_id=snapshot.camera_id,
        camera_name=snapshot.camera_name,
        source_type=snapshot.source_type,
        runtime_status=snapshot.runtime_status,
        capture_fps=snapshot.capture_fps,
        preview_fps=snapshot.preview_fps,
        inference_fps=None,
        frames_decoded=snapshot.frames_decoded,
        frames_published=snapshot.frames_published,
        frames_dropped_or_replaced=snapshot.frames_dropped_or_replaced,
        last_frame_at=snapshot.last_frame_at,
        last_frame_age_ms=snapshot.last_frame_age_ms,
        last_successful_open_at=snapshot.last_successful_open_at,
        last_error_at=snapshot.last_error_at,
        safe_error_code=snapshot.safe_error_code,
        read_failures=snapshot.read_failures,
        reconnect_count=snapshot.reconnect_count,
        current_backoff_seconds=snapshot.current_backoff_seconds,
        frame_width=snapshot.frame_width,
        frame_height=snapshot.frame_height,
        worker_running=snapshot.worker_running,
    )

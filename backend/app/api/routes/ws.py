"""Native FastAPI WebSocket routes for live event broadcasts and binary frame previews."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.camera.events import live_event_hub
from backend.app.camera.manager import camera_manager
from backend.app.core.config import settings
from backend.app.core.logging import logger

router = APIRouter(tags=["WebSockets"])


@router.websocket("/ws/live")
async def live_events_websocket(websocket: WebSocket) -> None:
    """Real-time JSON event fan-out endpoint broadcasting camera states and system telemetry."""
    await websocket.accept()
    queue = live_event_hub.subscribe(maxsize=50)

    try:
        # Initial handshake envelope
        await websocket.send_json({
            "event_type": "CONNECTION_ESTABLISHED",
            "message": "Connected to Presyn Live Event Broadcast",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        while True:
            event = await queue.get()
            await websocket.send_json(event)

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        logger.debug("Live events WebSocket client disconnected: %s", exc)
    finally:
        live_event_hub.unsubscribe(queue)


@router.websocket("/ws/cameras/{camera_id}/frames")
async def camera_frames_websocket(websocket: WebSocket, camera_id: int) -> None:
    """Dedicated binary preview WebSocket streaming newest JPEG frames with built-in backpressure."""
    await websocket.accept()

    worker = camera_manager.get_worker(camera_id)
    if worker is None or not worker.is_running():
        await websocket.send_json({
            "type": "STREAM_INFO",
            "camera_id": camera_id,
            "status": "OFFLINE",
            "message": "Camera capture worker is offline or not running.",
        })
    else:
        await websocket.send_json({
            "type": "STREAM_INFO",
            "camera_id": camera_id,
            "status": "STREAMING",
            "preview_fps": worker.preview_fps,
            "format": "jpeg",
        })

    last_sent_sequence = -1
    interval = 1.0 / max(1, settings.CAMERA_PREVIEW_FPS)

    try:
        while True:
            worker = camera_manager.get_worker(camera_id)
            if worker is not None and worker.is_running():
                preview_frame = worker.frame_buffer.get_latest_preview()
                if preview_frame is not None and preview_frame.sequence != last_sent_sequence:
                    last_sent_sequence = preview_frame.sequence
                    # Send JPEG bytes as binary WebSocket frame
                    await websocket.send_bytes(preview_frame.jpeg_bytes)

            await asyncio.sleep(interval)

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        logger.debug("Frame WebSocket client disconnected for camera_id=%d: %s", camera_id, exc)

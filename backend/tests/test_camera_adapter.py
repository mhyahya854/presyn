"""Unit tests for OpenCV capture adapter and mock hardware selection."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

from backend.app.camera.source import (
    FakeCaptureAdapter,
    OpenCVCaptureAdapter,
    get_capture_adapter,
    reset_capture_adapter_factory,
    set_capture_adapter_factory,
)


def test_fake_capture_adapter_lifecycle():
    """Verify synthetic fake capture adapter lifecycle without real hardware."""
    adapter = FakeCaptureAdapter(can_open=True, frame_width=320, frame_height=240, max_reads=3)

    assert not adapter.is_opened()
    assert adapter.open("dummy_source") is True
    assert adapter.is_opened()

    # Read 3 valid frames
    for i in range(3):
        success, frame = adapter.read()
        assert success is True
        assert frame is not None
        assert frame.shape == (240, 320, 3)

    # 4th read exceeds max_reads
    success, frame = adapter.read()
    assert success is False
    assert frame is None

    adapter.release()
    assert not adapter.is_opened()


def test_fake_capture_adapter_open_failure():
    """Verify fake capture adapter reports open failure when configured."""
    adapter = FakeCaptureAdapter(can_open=False)
    assert adapter.open("dummy_source") is False
    assert not adapter.is_opened()

    success, frame = adapter.read()
    assert success is False
    assert frame is None


def test_capture_adapter_factory_injection():
    """Verify custom capture adapter factory can be injected and reset cleanly."""
    reset_capture_adapter_factory()
    default_adapter = get_capture_adapter("RTSP")
    assert isinstance(default_adapter, OpenCVCaptureAdapter)

    # Inject mock factory
    fake_inst = FakeCaptureAdapter()
    set_capture_adapter_factory(lambda source_type: fake_inst)
    injected_adapter = get_capture_adapter("RTSP")
    assert injected_adapter is fake_inst

    # Reset
    reset_capture_adapter_factory()
    restored = get_capture_adapter("RTSP")
    assert isinstance(restored, OpenCVCaptureAdapter)


def test_opencv_adapter_windows_directshow_selection(monkeypatch):
    """Verify Windows webcam uses DirectShow backend if available."""
    monkeypatch.setattr(sys, "platform", "win32")

    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True

    with patch("cv2.VideoCapture", return_value=mock_cap) as mock_vc:
        adapter = OpenCVCaptureAdapter(source_type="WEBCAM")
        res = adapter.open(0)
        assert res is True
        assert mock_vc.called
        # Check cv2.CAP_DSHOW was passed as second argument if available
        import cv2
        if hasattr(cv2, "CAP_DSHOW"):
            call_args = mock_vc.call_args[0]
            assert len(call_args) >= 2
            assert call_args[1] == cv2.CAP_DSHOW


def test_opencv_adapter_rtsp_ffmpeg_selection():
    """Verify RTSP stream uses FFmpeg backend if available."""
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True

    with patch("cv2.VideoCapture", return_value=mock_cap) as mock_vc:
        adapter = OpenCVCaptureAdapter(source_type="RTSP")
        res = adapter.open("rtsp://192.168.1.50:554/live")
        assert res is True
        assert mock_vc.called
        import cv2
        if hasattr(cv2, "CAP_FFMPEG"):
            call_args = mock_vc.call_args[0]
            assert len(call_args) >= 2
            assert call_args[1] == cv2.CAP_FFMPEG


def test_capture_adapter_does_not_echo_secret_in_logs_on_failure(caplog):
    """Verify that capture open failure does not leak secret-bearing source URLs in log records."""
    adapter = OpenCVCaptureAdapter(source_type="RTSP")
    secret_url = "rtsp://secret_user:super_secret_password@192.168.1.1:554/feed"

    with patch("cv2.VideoCapture", side_effect=RuntimeError("Native connection error")):
        success = adapter.open(secret_url)
        assert success is False

    for record in caplog.records:
        assert "super_secret_password" not in record.message
        assert "secret_user" not in record.message

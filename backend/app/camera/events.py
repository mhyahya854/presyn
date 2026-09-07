"""Asynchronous event fan-out hub for live platform events."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import threading
from typing import Any, Dict, Optional, Set
import uuid


class LiveEventHub:
    """Thread-safe fan-out hub broadcasting live events to async WebSocket clients.

    - Worker threads publish without blocking.
    - Each client has a bounded queue (maxsize=50).
    - Slow clients drop older events rather than accumulating unbounded memory.
    """

    def __init__(self) -> None:
        self._subscribers: Set[asyncio.Queue[Dict[str, Any]]] = set()
        self._lock = threading.Lock()
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Register the running asyncio event loop."""
        self._loop = loop

    def subscribe(self, maxsize: int = 50) -> asyncio.Queue[Dict[str, Any]]:
        """Register a new WebSocket subscriber queue."""
        queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=maxsize)
        with self._lock:
            self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[Dict[str, Any]]) -> None:
        """Remove a disconnected WebSocket subscriber queue."""
        with self._lock:
            self._subscribers.discard(queue)

    def publish_from_thread(
        self,
        event_type: str,
        camera_id: int,
        camera_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Thread-safe entrypoint for background capture workers to broadcast events."""
        if not self._loop or not self._loop.is_running():
            return

        envelope = self.build_envelope(event_type, camera_id, camera_name, payload)

        try:
            asyncio.run_coroutine_threadsafe(self._broadcast(envelope), self._loop)
        except RuntimeError:
            pass

    async def _broadcast(self, envelope: Dict[str, Any]) -> None:
        """Deliver event to all connected subscriber queues, dropping old items if full."""
        with self._lock:
            subscribers = list(self._subscribers)

        for queue in subscribers:
            if queue.full():
                try:
                    queue.get_nowait()
                except (asyncio.QueueEmpty, ValueError):
                    pass
            try:
                queue.put_nowait(envelope)
            except asyncio.QueueFull:
                pass

    @staticmethod
    def build_envelope(
        event_type: str,
        camera_id: int,
        camera_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Construct a standardized event envelope adhering to the Master Plan contract."""
        return {
            "event_id": f"evt_{uuid.uuid4()}",
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "camera_id": camera_id,
            "camera_name": camera_name,
            "payload": payload or {},
            "spatial": None,
            "face": None,
            "identity": None,
            "verification": None,
            "activity": None,
            "optional_features": None,
            "system_state": {
                "visitor_mode": False,
                "attendance_action_triggered": None,
                "warning": None,
            },
        }

    def shutdown(self) -> None:
        """Clear all active subscriber queues on application shutdown."""
        with self._lock:
            self._subscribers.clear()


# Global singleton instance of the LiveEventHub
live_event_hub = LiveEventHub()

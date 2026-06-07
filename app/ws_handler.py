"""
ws_handler.py — Safe WebSocket connection manager with timeout and max limit.
"""
import asyncio
import logging
from fastapi import WebSocket

log = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self, max_connections: int = 100, timeout_seconds: int = 30):
        self.active: dict[str, WebSocket] = {}
        self.max_connections = max_connections
        self.timeout_seconds = timeout_seconds

    async def connect(self, websocket: WebSocket, client_id: str):
        if len(self.active) >= self.max_connections:
            await websocket.close(code=1008, reason="Server at capacity")
            log.warning("Rejected WS connection — at capacity (%d)", self.max_connections)
            return
        await websocket.accept()
        self.active[client_id] = websocket
        log.info("WS connected: %s (total=%d)", client_id, len(self.active))

    def disconnect(self, client_id: str):
        self.active.pop(client_id, None)
        log.info("WS disconnected: %s (total=%d)", client_id, len(self.active))

    async def broadcast(self, message: str):
        dead = []
        for cid, ws in self.active.items():
            try:
                await asyncio.wait_for(ws.send_text(message), timeout=self.timeout_seconds)
            except Exception:
                dead.append(cid)
        for cid in dead:
            self.disconnect(cid)

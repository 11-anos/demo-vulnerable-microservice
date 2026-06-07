"""
main.py — FastAPI microservice entrypoint.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from contextlib import asynccontextmanager
import logging
import os

from app.db import get_db_connection, close_db_pool
from app.ws_handler import WebSocketManager
from app.config import Settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
settings = Settings()
ws_manager = WebSocketManager(max_connections=100, timeout_seconds=30)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up — initialising DB pool")
    yield
    log.info("Shutting down — closing DB pool")
    await close_db_pool()


app = FastAPI(title="User Analytics Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT id, name, email FROM users WHERE id = $1",
            user_id  # parameterized — safe
        )
    if not row:
        return {"error": "not found"}
    return dict(row)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"[{client_id}]: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
    finally:
        # Always clean up — prevents file descriptor leaks
        ws_manager.disconnect(client_id)

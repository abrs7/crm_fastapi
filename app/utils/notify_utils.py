from fastapi.encoders import jsonable_encoder
import asyncio
from typing import List
from fastapi import WebSocket

# Store active WebSocket connections
active_connections: List[WebSocket] = []

async def notify_clients(message: dict):
    """Send real-time notifications to all connected clients"""
    for connection in active_connections:
        await connection.send_json(message)

import pytest
from httpx import AsyncClient
from fastapi import WebSocketDisconnect
from app.main import app
from app.models import UserRole
import websockets

@pytest.mark.asyncio
async def test_websocket_notifications(client):
    """Test WebSocket connection and real-time notifications"""
    async with websockets.connect("ws://localhost:8000/ws/notifications") as ws:
        
        #Login to test user account
        response = await client.post(
            "/token", 
            data={"username": "testuser", "password": "testpassword"}
        )
        assert response.status_code == 200
        access_token = response.json().get("access_token")
            
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await client.patch(
            "/api/leads/1/status", 
            json={"new_status": "closed"}, headers=headers
        )
        assert response.status_code == 200

        # Now listen for the notifications
        message = await ws.recv()
        
        # Assert that the message is in the expected format
        assert message is not None
        assert isinstance(message, str)

        
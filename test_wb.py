import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/notifications"  # Adjust if your server is running on a different port
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to WebSocket")

        # Wait for messages from the server
        try:
            while True:
                message = await websocket.recv()
                print("📩 Received:", message)
        except websockets.exceptions.ConnectionClosed:
            print("❌ WebSocket connection closed")

# Run the test
asyncio.run(test_websocket())

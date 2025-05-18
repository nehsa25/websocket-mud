import pytest
import websockets
import json

from core.interfaces import websocket



@pytest.fixture
def anyio_backend() -> str:
    """
    AnyIO backend fixture.
    """
    return "asyncio"


# Test function for the "new user as a guest" login scenario
@pytest.mark.asyncio
async def test_new_user_gets_username_request():
    uri = "ws://localhost:22009/"

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"type": "login", "username": "guest"}))

            # Receive the response
            response = await websocket.recv()
            response_data = json.loads(response)

            # Verify
            assert response_data["type"] == "username_request"
    except Exception:
        # Handle any exceptions that occur during the test
        pytest.fail("WebSocket connection failed or unexpected error occurred.")
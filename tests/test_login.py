import pytest
import websockets
import json

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
            # Receive the response
            response = await websocket.recv()
            response_data = json.loads(response)

            # Verify
            assert response_data["type"] == "username_request"
    except Exception:
        # Handle any exceptions that occur during the test
        pytest.fail("WebSocket connection failed or unexpected error occurred.")

# Test function for the "new user as a guest" login scenario
@pytest.mark.asyncio
async def test_new_user_login_guest():
    uri = "ws://localhost:22009/"

    try:
        async with websockets.connect(uri) as websocket:
            # Receive the response
            connection_respones = await websocket.recv()
            connection_response_data = json.loads(connection_respones)

            # Verify
            assert connection_response_data["type"] == "username_request"

            # register as guest
            await websocket.send(json.dumps({"type": "username_answer", "username": "guest"}))

            # Receive the response
            guest_response = await websocket.recv()
            guest_response_data = json.loads(guest_response)

            # Verify
            assert guest_response_data["type"] == "welcome"
            assert guest_response_data["character"]["firstname"] == "Guest"
            assert guest_response_data["character"]["lastname"] == "Character"
            assert guest_response_data["character"]["level"] == 1
            assert guest_response_data["character"]["money"] == 0
            assert guest_response_data["character"]["experience"] == 0


    except Exception:
        # Handle any exceptions that occur during the test
        pytest.fail("WebSocket connection failed or unexpected error occurred.")
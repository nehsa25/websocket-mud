import asyncio
import base64
import requests
import websockets
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class AIImages(Utility):
    def __init__(self, logger) -> None:
        LogUtils.debug("Initializing AIImages() class", logger)
        self.logger = logger

        
    def start_async(self, room_image_name, room_description, player):
        start_server = self.generate_room_image(room_image_name, room_description, player)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        
    async def generate_room_image(self, room_image_name, room_description, player):
        engine_id = "stable-diffusion-v1-6"
        api_host = 'https://api.stability.ai'
        api_key = "sk-aIIMUE6NJeYvXfmJ83d8T6Rqueur7hOjT07hskStmrnB7khw"

        if api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": room_description
                    }
                ],
                "cfg_scale": 35,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30,
                "style_present": "fantasy-art"
                },
            )
        
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(room_image_name, "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        # send room image event
        map_event = MudEvents.RoomImageEvent(room_image_name).to_json()
        self.send_message_sync(map_event, player.websocket)
        
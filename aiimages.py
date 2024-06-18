import asyncio
import base64
import requests
import websockets
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class GeneratedFileType(Utility):
    description = None
    file_name = None
    
    def __init__(self, line, logger) -> None:
        LogUtils.debug("Initializing GeneratedFileType() class", logger)
        line_items = line.split("!!!")
        file_name = line_items[0]
        description = line_items[1]
        self.logger = logger
        self.description = description
        self.file_name = file_name

class AIImages(Utility):
    def __init__(self, logger) -> None:
        LogUtils.debug("Initializing AIImages() class", logger)
        self.logger = logger

    def start_async(self, room_image_name, room_description, player):
        start_server = self.generate_room_image(room_image_name, room_description, player)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(start_server)
        
    async def generate_room_image(self, room_image_name, room_description, player):
        image_name = ""
        # get already generated rooms
        with open("ai_rooms.txt", "r") as text_file:
            contents = text_file.readlines()            
            for line in contents:
                item = GeneratedFileType(line, self.logger)
                if item.description.strip() == room_description.strip():
                    image_name = item.file_name
                    break
        
        # only generate a room if one isn't already generated
        if image_name == "":
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
                    "cfg_scale": 25,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                    "style_present": "pixel-art"
                    },
                )
            
            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))

            data = response.json()

            self.path = f"c:/src/mud_images"
            full_path = f"{self.path}/{room_image_name}"
            for i, image in enumerate(data["artifacts"]):
                with open(full_path, "wb") as f:
                    f.write(base64.b64decode(image["base64"]))

            # save the room image to the file 
            with open("ai_rooms.txt", "a") as text_file:
                text_file.write(room_image_name + "!!!" + room_description + "\n")
        else:
            room_image_name = image_name
            
        # send room image event
        await self.send_message(MudEvents.RoomImageEvent(room_image_name), player.websocket)
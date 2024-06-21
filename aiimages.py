import os
import requests
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
        
    async def create_seed(self):
        seed = 0
        for letter in enumerate("ethandrakestone"):
            seed += ord(letter[1])
        return seed

    async def generate_room_image(self, room_image_name, room_description, inside, player, world):
        image_name = ""
        
        # update rooms description with weather
        if not inside:
            room_description = world.weather.add_weather_description(room_description)
            
        # get already generated rooms
        with open("ai_rooms.txt", "r") as text_file:
            contents = text_file.readlines()            
            for line in contents:
                item = GeneratedFileType(line, self.logger)
                if item.description.strip() == room_description.strip():
                    image_name = item.file_name
                    break
        
        # only generate a room if one isn't already generated
        seed = await self.create_seed()
        if image_name == "":
            engine_id = "stable-diffusion-v1-6"
            api_host = f"https://api.stability.ai",
            api_key = "sk-aIIMUE6NJeYvXfmJ83d8T6Rqueur7hOjT07hskStmrnB7khw"

            if api_key is None:
                raise Exception("Missing Stability API key.")
            headers={
                    "authorization": f"Bearer {api_key}",
                    "accept": "image/*"
                }
            response = requests.post(
                f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
                headers=headers,
                files={"none": ''},
                data={
                    "prompt":  "pixelated " + room_description,
                    "seed": seed
                }
            )
        
            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))
       
            self.path = f"c:/src/mud_images/rooms"
            full_path = f"{self.path}/{room_image_name}"            
            if os.path.exists(full_path):
                os.remove(full_path)
                
            with open(full_path, "wb") as f:
                f.write(response.content)

            # save the room image to the file 
            with open("ai_rooms.txt", "a") as text_file:
                text_file.write(room_image_name + "!!!" + room_description + "\n")
        else:
            room_image_name = image_name
            
        # send room image event
        await self.send_message(MudEvents.RoomImageEvent(room_image_name), player.websocket)
from enum import Enum
import inspect
import json
import os
import jsonpickle
import requests
from dontcheckin import Secrets
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class GeneratedFileType(Utility):
    description = None
    file_name = None
    secrets = None
    
    def __init__(self, line, logger) -> None:
        LogUtils.debug("Initializing GeneratedFileType() class", logger)
        item = json.loads(line)
        self.logger = logger
        self.description = item["description"]
        self.file_name = item["file_name"]

class AIImages(Utility):   
    style = None
    secrets = Secrets()
    generator = None
    seed = None
       
    class StabilityAPI:
        logger = None
        key = None
        seed = None
        def __init__(self, seed, logger) -> None:
            self.logger = logger
            LogUtils.debug("Initializing StabilityAIAPI() class", self.logger)            
            self.key = Secrets.StabilityAIKey
            self.seed = seed
            
        def create(self, seed, description, room_image_name):
            return self.create_sd3_medium(seed, description, room_image_name)
            
        def create_sd3_medium(self, seed, description, room_image_name):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            api_key = self.key
            full_path = "" 
            if api_key is None:
                raise Exception("Missing Stability API key.")
            headers={
                    "authorization": f"Bearer {api_key}",
                    "accept": "image/*"
                }
            response = requests.post(
                f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
                headers=headers,
                files={"none": ''},
                data={
                    "prompt":  "pixelated,medieval,gothic,scary, and " + description,
                    "seed": seed,
                    "model": "sd3-large-turbo",
                    "output_format": "png"
                }
            )            
            if response.status_code == 200:
                self.path = f"c:/src/mud_images/rooms"
                full_path = f"{self.path}/{room_image_name}"   
                if os.path.exists(full_path):
                    os.remove(full_path)
                    
                with open(full_path, "wb") as f:
                    f.write(response.content)
            elif response.status_code == 402:
                    LogUtils.warn(f"AI image could not be generated via Stability AI", self.logger)
            else:
                LogUtils.error(f"Non-200 response: {str(response.text)}", self.logger)   
                                  
            LogUtils.debug(f"{method_name}: exit", self.logger)
            return full_path
        
        def create_ultra(self, seed, description, room_image_name):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            api_key = self.key
            full_path = "" 
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
                    "prompt":  "pixelated " + description,
                    "seed": seed
                }
            )            
            if response.status_code == 200:
                self.path = f"c:/src/mud_images/rooms"
                full_path = f"{self.path}/{room_image_name}"   
                if os.path.exists(full_path):
                    os.remove(full_path)
                    
                with open(full_path, "wb") as f:
                    f.write(response.content)
            elif response.status_code == 402:
                    LogUtils.warn(f"AI image could not be generated via {self.style}", self.logger)
            else:
                LogUtils.error(f"Non-200 response: {str(response.text)}", self.logger)   
                                  
            LogUtils.debug(f"{method_name}: exit", self.logger)
            return full_path
            
    class LogEntry:
        file_name = None
        description = None        
        def __init__(self, file_name, description) -> None:
            self.file_name = file_name
            self.description = description            
        def to_json(self):
            return jsonpickle.encode(self)

    def __init__(self, logger,  style=Utility.Share.AIGeneration.StabilityAI) -> None:
        LogUtils.debug("Initializing AIImages() class", logger)
        self.logger = logger
        
        # super seed!
        self.seed = self.create_seed()        
        
        if style == Utility.Share.AIGeneration.GeminiAI:
            self.generator = self.GeminiAPI(self.seed, logger)
        elif style == Utility.Share.AIGeneration.StabilityAI:
            self.generator = self.StabilityAPI(self.seed, logger)
        
    def create_seed(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        seed = 0
        for letter in enumerate("ethandrakestone + 12141999"):
            seed += ord(letter[1])
        LogUtils.info(f"{method_name}: image seed: {seed}", self.logger)
        LogUtils.debug(f"{method_name}: exit, seed: {seed}", self.logger)
        return seed    

    def add_log_entry(self, log_name, file_name, description):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        entry = AIImages.LogEntry(file_name, description).to_json()
        bytes_written = 0
        with open(log_name, "a") as text_file:
            bytes_written = text_file.write(f"{entry}\n")
        LogUtils.info(f"{method_name}: image bytes written: {bytes_written}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    def read_log_entries(self, description, log_name):  
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        result = None  
        with open(log_name, "r") as text_file:
            contents = text_file.readlines()            
            for line in contents:
                entry = AIImages.LogEntry(line)
                if entry.description == description:
                    result = entry.file_name
        LogUtils.info(f"{method_name}: found: {True if result is not None else False}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return result
                
    async def generate_image(self, item_name, item_description, player, world_state, inside=False, type=Utility.Share.ImageType.ROOM):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        image_name = ""        
        item_description = item_description.strip()
        log_name = ""
        
        
        if type == Utility.Share.ImageType.ROOM:
            log_name = "ai_rooms.txt"

            # update rooms description with weather
            if not inside:
                item_description = world_state.weather.add_weather_description(item_description)
                
            # get already generated rooms
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = GeneratedFileType(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.Share.ImageType.ITEM:
            log_name = "ai_items.txt"
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = GeneratedFileType(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.Share.ImageType.PLAYER:
            log_name = "ai_players.txt"
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = GeneratedFileType(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.Share.ImageType.NPC:
            log_name = "ai_npcs.txt"
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = GeneratedFileType(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.Share.ImageType.MONSTER:
            log_name = "ai_monsters.txt"
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = GeneratedFileType(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
                    
        # only generate a room if one isn't already generated
        if image_name == "":
            LogUtils.info("Cannot find image for description:", self.logger)
            LogUtils.info(item_description, self.logger)
            
            path = self.generator.create(self.seed, item_description, item_name)
            if path is not None and path != "":
                # save the room image to the file 
                self.add_log_entry(log_name, item_name, item_description)
            else:
                item_name = "noimage.jpg"
        else:
            item_name = image_name
            
        # send room image event
        if type == Utility.Share.ImageType.ROOM:
            await self.send_message(MudEvents.RoomImageEvent(item_name), player.websocket)
        elif type == Utility.Share.ImageType.ITEM:
            await self.send_message(MudEvents.ItemImageEvent(item_name), player.websocket)
        elif type == Utility.Share.ImageType.PLAYER:
            await self.send_message(MudEvents.PlayerImageEvent(item_name), player.websocket)
        elif type == Utility.Share.ImageType.NPC:
            await self.send_message(MudEvents.NpcImageEvent(item_name), player.websocket)
        elif type == Utility.Share.ImageType.MONSTER:
            await self.send_message(MudEvents.MonsterImageEvent(item_name), player.websocket)
                    


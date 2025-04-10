from enum import Enum
import inspect
import json
import os
import jsonpickle
import requests
from dontcheckin import DevSettings, Secrets, WorldSettings
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility
from utilities.aws import S3Utils

# 
class AIFile(Utility):
    description = None
    file_name = None
    logger = None

    def __init__(self, line, logger) -> None:
        item = json.loads(line)
        self.logger = logger
        self.description = item["description"]
        self.file_name = item["file_name"]

class AIImages(Utility):   
    style = None
    secrets = Secrets()
    generator = None
    seed = None
       
    class OpenAIAPI:
        logger = None
        key = None
        seed = None
        def __init__(self, seed, logger) -> None:
            self.logger = logger
            LogUtils.debug("Initializing StabilityAIAPI() class", self.logger)            
            self.key = Secrets.StabilityAIKey
            self.seed = seed

        def create_room(self, seed, description, image_name):
            image_name = self.santitize_filename(image_name)
            path = f"{DevSettings.data_location}/mud-images/rooms"
            prompt = WorldSettings.room_tone + description
            return self.create_sd3_medium(prompt, seed, path, image_name)
        
        def create_item(self, seed, description, image_name):
            image_name = self.santitize_filename(image_name)
            path = f"{DevSettings.data_location}/mud-images/items"
            prompt = WorldSettings.item_tone + description
            return self.create_sd3_medium(prompt, seed, path, image_name)
        
        def create_player(self, seed, description, image_name):
            image_name = self.santitize_filename(image_name)
            path = f"{DevSettings.data_location}/mud-images/players"
            prompt = WorldSettings.player_tone + description
            return self.create_sd3_medium(prompt, seed, path, image_name)
        
        def create_npc(self, seed, description, image_name):
            image_name = self.santitize_filename(image_name)
            path = f"{DevSettings.data_location}/mud-images/npcs"
            prompt = WorldSettings.npc_tone + description
            npc_name = self.create_sd3_medium(prompt, seed, path, image_name)
            return npc_name
        
        def create_monster(self, seed, description, image_name):
            image_name = self.santitize_filename(image_name)
            path = f"{DevSettings.data_location}/mud-images/monsters"
            prompt = WorldSettings.monster_tone + description
            return self.create_sd3_medium(prompt, seed, path, image_name)
        
        def santitize_filename(self, file_name):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            file_name = file_name.replace(" ", "_")
            file_name = file_name.replace(":", "")
            file_name = file_name.replace(",", "")
            file_name = file_name.replace("!", "")
            file_name = file_name.replace("?", "")
            LogUtils.debug(f"{method_name}: exit", self.logger)
            return file_name
        
        def create_sd3_medium(self, prompt, seed, path, name):
            try:
                method_name = inspect.currentframe().f_code.co_name
                LogUtils.debug(f"{method_name}: enter", self.logger)
                name = self.santitize_filename(name)
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
                        "prompt": prompt,
                        "seed": seed,
                        "model": "sd3-large-turbo",
                        "output_format": "png"
                    }
                )            
                if response.status_code == 200:
                    full_path = os.path.join(path, name)   
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        
                    # ensure path exists
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)

                    with open(full_path, "w+b") as f:
                        f.write(response.content)
                elif response.status_code == 402:
                        LogUtils.warn(f"AI image could not be generated via Stability AI", self.logger)
                else:
                    LogUtils.error(f"Non-200 response: {str(response.text)}", self.logger)   
                                    
                LogUtils.debug(f"{method_name}: exit", self.logger)
                return full_path
            except Exception as e:
                LogUtils.error(f"Error: {str(e)}", self.logger)
                raise e
        
        # def create_ultra(self, seed, description, room_image_name):
        #     method_name = inspect.currentframe().f_code.co_name
        #     LogUtils.debug(f"{method_name}: enter", self.logger)
        #     api_key = self.key
        #     full_path = "" 
        #     if api_key is None:
        #         raise Exception("Missing Stability API key.")
        #     headers={
        #             "authorization": f"Bearer {api_key}",
        #             "accept": "image/*"
        #         }
        #     response = requests.post(
        #         f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        #         headers=headers,
        #         files={"none": ''},
        #         data={
        #             "prompt":  "pixelated " + description,
        #             "seed": seed
        #         }
        #     )            
        #     if response.status_code == 200:
        #         self.path = f"c:/src/mud_images/rooms"
        #         full_path = f"{self.path}/{room_image_name}"   
        #         if os.path.exists(full_path):
        #             os.remove(full_path)
                    
        #         with open(full_path, "wb") as f:
        #             f.write(response.content)
        #     elif response.status_code == 402:
        #             LogUtils.warn(f"AI image could not be generated via {self.style}", self.logger)
        #     else:
        #         LogUtils.error(f"Non-200 response: {str(response.text)}", self.logger)   
                                  
        #     LogUtils.debug(f"{method_name}: exit", self.logger)
        #     return full_path
            
    class LogEntry:
        file_name = None
        description = None        
        def __init__(self, file_name, description) -> None:
            self.file_name = file_name
            self.description = description            
        def to_json(self):
            return jsonpickle.encode(self)

    def __init__(self, logger,  style=Utility.AIGeneration.OpenAI) -> None:
        LogUtils.debug("Initializing AIImages() class", logger)
        self.logger = logger
        
        # super seed!
        self.seed = self.create_seed()        
        
        if style == Utility.AIGeneration.GeminiAI:
            self.generator = self.GeminiAPI(self.seed, logger)
        elif style == Utility.AIGeneration.OpenAI:
            self.generator = self.OpenAIAPI(self.seed, logger)
        
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
    
    def santitize(self, file_name):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        file_name = file_name.replace(" ", "_")
        file_name = file_name.replace(":", "")
        file_name = file_name.replace(",", "")
        file_name = file_name.replace("!", "")
        file_name = file_name.replace("?", "")
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return file_name
    
    def get_data_file_name(self, type, tone):
        return f"{type}_{self.santitize(tone)}.dat"
                
    async def generate_image(self, 
                            item_name, 
                            item_description, 
                            player, 
                            world_state, 
                            inside=False, 
                            type=Utility.ImageType.ROOM):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        image_name = ""        
        item_description = item_description.strip()
        log_name = ""        
        
        if type == Utility.ImageType.ROOM:
            log_name = self.get_data_file_name(Utility.ImageType.ROOM, WorldSettings.room_tone)

            # update rooms description with weather
            if not inside:
                item_description = world_state.weather.add_weather_description(item_description)
                
            # get already generated rooms
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = AIFile(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.ImageType.ITEM:
            log_name = self.get_data_file_name(Utility.ImageType.ITEM, WorldSettings.player_tone)
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = AIFile(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.ImageType.PLAYER:
            log_name = self.get_data_file_name(Utility.ImageType.PLAYER, WorldSettings.player_tone)
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = AIFile(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.ImageType.NPC:
            log_name = self.get_data_file_name(Utility.ImageType.NPC, WorldSettings.player_tone)
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = AIFile(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
        elif type == Utility.ImageType.MONSTER:
            log_name = self.get_data_file_name(Utility.ImageType.MONSTER, WorldSettings.player_tone)
            if os.path.exists(log_name):
                with open(log_name, "r") as text_file:
                    contents = text_file.readlines()            
                    for line in contents:
                        item = AIFile(line, self.logger)
                        if item.description.strip() == item_description:
                            image_name = item.file_name
                            break
                    
        # only generate a object if one isn't already generated
        if image_name == "":
            LogUtils.info("Cannot find image for description:", self.logger)
            LogUtils.info(item_description, self.logger)
            
            if type == Utility.ImageType.ROOM:
                path = self.generator.create_room(self.seed, item_description, item_name)
            elif type == Utility.ImageType.ITEM:
                path = self.generator.create_item(self.seed, item_description, item_name)
            elif type == Utility.ImageType.PLAYER:
                path = self.generator.create_player(self.seed, item_description, item_name)
            elif type == Utility.ImageType.NPC:
                path = self.generator.create_npc(self.seed, item_description, item_name)
            elif type == Utility.ImageType.MONSTER:
                path = self.generator.create_monster(self.seed, item_description, item_name)

            # a new image was created
            if path is None or path == "":   
                LogUtils.error("Image generation failed", self.logger)
                raise Exception("Image generation failed")
        
            # save the room image to the file              
            self.add_log_entry(log_name, item_name, item_description)

            # upload s3
            s3_key = f"public/images/{str(type)}/{image_name}"
            image_url = S3Utils.upload_image_to_s3(path, s3_key)

            if image_url:
                print(f"Image uploaded successfully. Public URL: {image_url}")
                # Return this URL to your frontend
            else:
                print("Image upload failed.")
                
            # send room image event
            if type == Utility.ImageType.ROOM:
                await self.send_message(MudEvents.RoomImageEvent(item_name), player.websocket)
            elif type == Utility.ImageType.ITEM:
                await self.send_message(MudEvents.ItemImageEvent(item_name), player.websocket)
            elif type == Utility.ImageType.PLAYER:
                await self.send_message(MudEvents.PlayerImageEvent(item_name), player.websocket)
            elif type == Utility.ImageType.NPC:
                await self.send_message(MudEvents.NpcImageEvent(item_name), player.websocket)
            elif type == Utility.ImageType.MONSTER:
                await self.send_message(MudEvents.MonsterImageEvent(item_name), player.websocket)
                        


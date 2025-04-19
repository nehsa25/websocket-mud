import inspect
import json
import os
import jsonpickle
from ai.file import AIFile
from ai.services.gemini import GeminiAPI
from ai.services.openai import OpenAIAPI
from dontcheckin import Secrets
from ai.prompt import PromptSettings
from log_utils import LogUtils
from mudevent import MudEvents
from settings.exception import ExceptionUtils
from settings.settings import MudSettings
from utility import Utility
from utilities.aws import S3Utils

class AIImages(Utility):   
    style = None
    secrets = Secrets()
    generator = None
    seed = None

    class LogEntry:
        file_name = None
        description = None        
        def __init__(self, file_name, description) -> None:
            self.file_name = file_name
            self.description = description            
        def to_json(self):
            return jsonpickle.encode(self)

    def __init__(self, logger) -> None:
        LogUtils.debug("Initializing AIImages() class", logger)
        self.logger = logger

        # super seed!
        self.seed = self.create_seed()  

        style = MudSettings.image_generation_technology
        if style == Utility.AIGeneration.GeminiAI:
            self.generator = GeminiAPI(self.seed, logger)
        elif style == Utility.AIGeneration.OpenAI:
            self.generator = OpenAIAPI(self.seed, logger)
     
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
    
    def clean_file_name(self, tone_description):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        tone_description = ', '.join(tone_description)
        tone_description = tone_description.replace(" ", "_")
        tone_description = tone_description.replace(":", "")
        tone_description = tone_description.replace(",", "")
        tone_description = tone_description.replace("[", "")
        tone_description = tone_description.replace("]", "")
        tone_description = tone_description.replace("'", "")
        tone_description = tone_description.replace("!", "")
        tone_description = tone_description.replace("?", "")
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return tone_description
    
    def get_data_file_name(self, type, tone):
        file = f"{type}_{self.clean_file_name(tone["style"])}.dat"
        LogUtils.debug(f"Returning filename: {file}", self.logger)
        return file
                
    async def generate_image(self, 
                            item_name, 
                            item_description, 
                            player, 
                            world_state, 
                            inside=False, 
                            type=Utility.ImageType.ROOM):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        try:
            image_name = ""        
            item_description = item_description.strip()
            log_name = ""        
            
            if type == Utility.ImageType.ROOM:
                log_name = self.get_data_file_name(Utility.ImageType.ROOM, PromptSettings.room_tone)

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
                log_name = self.get_data_file_name(Utility.ImageType.ITEM, PromptSettings.player_tone)
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()            
                        for line in contents:
                            item = AIFile(line, self.logger)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Utility.ImageType.PLAYER:
                log_name = self.get_data_file_name(Utility.ImageType.PLAYER, PromptSettings.player_tone)
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()            
                        for line in contents:
                            item = AIFile(line, self.logger)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Utility.ImageType.NPC:
                log_name = self.get_data_file_name(Utility.ImageType.NPC, PromptSettings.player_tone)
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()            
                        for line in contents:
                            item = AIFile(line, self.logger)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Utility.ImageType.MONSTER:
                log_name = self.get_data_file_name(Utility.ImageType.MONSTER, PromptSettings.player_tone)
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
                    path = await self.generator.create_room(self.seed, item_description, item_name)
                elif type == Utility.ImageType.ITEM:
                    path = await self.generator.create_item(self.seed, item_description, item_name)
                elif type == Utility.ImageType.PLAYER:
                    path = await self.generator.create_player(self.seed, item_description, item_name)
                elif type == Utility.ImageType.NPC:
                    path = await self.generator.create_npc(self.seed, item_description, item_name)
                elif type == Utility.ImageType.MONSTER:
                    path = await self.generator.create_monster(self.seed, item_description, item_name)

                # a new image was created
                if path is None or path == "":   
                    LogUtils.error("Image generation failed", self.logger)
                    raise Exception("Image generation failed")
        
                # upload s3
                s3_key = f"public/images/rooms/{item_name}"
                S3Utils.upload_image_to_s3(path, s3_key, 
                                                       make_public=True, 
                                                         content_type='image/png', 
                                                         logger=self.logger)
                
                image_url = S3Utils.generate_public_url(s3_key)
                if image_url:
                    print(f"Image uploaded successfully. Public URL: {image_url}")          
                    self.add_log_entry(log_name, s3_key, item_description)
                else:
                    print("Image upload failed.")
                    
                # send room image event
                if type == Utility.ImageType.ROOM:
                    await self.send_message(MudEvents.RoomImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.ITEM:
                    await self.send_message(MudEvents.ItemImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.PLAYER:
                    await self.send_message(MudEvents.PlayerImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.NPC:
                    await self.send_message(MudEvents.NpcImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.MONSTER:
                    await self.send_message(MudEvents.MonsterImageEvent(image_url), player.websocket)

            else:
                LogUtils.info("Image already exists:", self.logger)
                LogUtils.info(image_name, self.logger)
                image_url = S3Utils.generate_public_url(image_name)
                if type == Utility.ImageType.ROOM:
                    await self.send_message(MudEvents.RoomImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.ITEM:
                    await self.send_message(MudEvents.ItemImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.PLAYER:
                    await self.send_message(MudEvents.PlayerImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.NPC:
                    await self.send_message(MudEvents.NpcImageEvent(image_url), player.websocket)
                elif type == Utility.ImageType.MONSTER:
                    await self.send_message(MudEvents.MonsterImageEvent(image_url), player.websocket)
        
        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)



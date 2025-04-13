import inspect
import json
import os
import requests
from ai.prompt import PromptSettings
from dontcheckin import Secrets
from log_utils import LogUtils
from settings.exception import ExceptionUtils
from settings.settings import MudSettings

class OpenAIAPI:
    logger = None
    key = None
    seed = None
    def __init__(self, seed, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing StabilityAIAPI() class", self.logger)            
        self.key = Secrets.StabilityAIKey
        self.seed = seed

    async def create_room(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/rooms"
        prompt = PromptSettings.generate_prompt(PromptSettings.room_tone, description)
        return await self.generate_image(prompt, seed, path, image_name)
    
    async def create_item(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/items"
        prompt = PromptSettings.generate_prompt(PromptSettings.item_tone, description)
        return await self.generate_image(prompt, seed, path, image_name)
    
    async def create_player(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/players"
        prompt = PromptSettings.generate_prompt(PromptSettings.player_tone, description)
        return await self.generate_image(prompt, seed, path, image_name)
    
    async def create_npc(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/npcs"
        prompt = PromptSettings.generate_prompt(PromptSettings.npc_tone, description)
        return await self.generate_image(prompt, seed, path, image_name)

    async def create_monster(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/monsters"
        prompt = PromptSettings.generate_prompt(PromptSettings.monster_tone, description)
        return await self.generate_image(prompt, seed, path, image_name)
    
    def clean_filename(self, file_name):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        file_name = file_name.replace(" ", "_")
        file_name = file_name.replace(":", "")
        file_name = file_name.replace(",", "")
        file_name = file_name.replace("!", "")
        file_name = file_name.replace("?", "")
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return file_name
    
    async def generate_image(self, prompt, seed, path, name):
        return await self.create_sd3_medium(prompt, seed, path, name)

    async def create_sd3_medium(self, prompt, seed, path, name):
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            prompt_string = json.dumps(prompt)
            name = self.clean_filename(name)
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
                    "prompt": prompt_string,
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
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
            raise e
        
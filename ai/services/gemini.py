import inspect
import json
import os
import requests
import google.generativeai as genai
from ai.prompt import PromptSettings
from dontcheckin import Secrets
from log_utils import LogUtils
from settings.exception import ExceptionUtils
from settings.settings import MudSettings

class GeminiAPI:
    logger = None
    key = None
    seed = None
    model = None

    def __init__(self, seed, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing GeminiAPI() class", self.logger)
        self.key = Secrets.GeminiAPIKey
        self.seed = seed

        # Configure the Gemini API
        genai.configure(api_key=self.key)

        # Select the Gemini model
        self.model = genai.GenerativeModel(MudSettings.geminiAImodel)

        # print models
        self.list_models()

    async def create_room(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/rooms"
        prompt = PromptSettings.generate_prompt(PromptSettings.room_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_item(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/items"
        prompt = PromptSettings.generate_prompt(PromptSettings.item_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_player(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/players"
        prompt = PromptSettings.generate_prompt(PromptSettings.player_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_npc(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/npcs"
        prompt = PromptSettings.generate_prompt(PromptSettings.npc_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_monster(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{MudSettings.data_location}/mud-images/monsters"
        prompt = PromptSettings.monster_tone + description
        prompt = PromptSettings.generate_prompt(PromptSettings.monster_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

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

    async def generate_gemini_image(self, prompt, seed, path, name):
        try:
            method_name = inspect.currentframe().f_code.co_name
            prompt = json.dumps(prompt)
            LogUtils.debug(f"{method_name}: enter", self.logger)
            name = self.clean_filename(name)
            full_path = ""

            if not self.model:
                raise Exception("Gemini model not initialized.")

            # Generate content using the Gemini model
            # response = self.model.generate_content(prompt)
            response = await self.model.generate_content_async(prompt)

            if response.parts:
                image_part = response.parts[0]
                if image_part.mime_type.startswith("image/"):
                    image_bytes = image_part.data
                    # Save the image to a file
                    with open("generated_image_imagen3.jpg", "wb") as f:
                        f.write(image_bytes)
                    print("Generated image saved as generated_image_imagen3.jpg")
                else:
                    print(f"Response text: {response.text}")
            else:
                LogUtils.warn(f"Gemini did not generate an image.", self.logger)
                return None

            LogUtils.debug(f"{method_name}: exit", self.logger)
            return full_path

        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
            raise e

    def list_models(self):
        """Lists available Gemini models and their capabilities."""
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)

            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    LogUtils.info(f"Model Name: {m.name}, Supported Methods: {m.supported_generation_methods}", self.logger)

        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
        finally:
            LogUtils.debug(f"{method_name}: exit", self.logger)
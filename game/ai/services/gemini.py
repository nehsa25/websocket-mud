import json
import google.generativeai as genai
from game.ai.services.prompt import PromptSettings
from dontcheckin import Secrets
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
from settings.global_settings import GlobalSettings


class GeminiAPI:
    logger = None
    key = None
    seed = None
    model = None

    def __init__(self, seed) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing GeminiAPI() class")
        self.key = Secrets.GeminiAPIKey
        self.seed = seed

        # Configure the Gemini API
        genai.configure(api_key=self.key)

        # Select the Gemini model
        self.model = genai.GenerativeModel(GlobalSettings.GEMINI_AI_MODEL)

        # print models
        self.list_models()

    async def create_room(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{GlobalSettings.DATA_LOCATION}/mud-images/rooms"
        prompt = PromptSettings.generate_prompt(PromptSettings.room_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_item(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{GlobalSettings.DATA_LOCATION}/mud-images/items"
        prompt = PromptSettings.generate_prompt(PromptSettings.item_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_player(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{GlobalSettings.DATA_LOCATION}/mud-images/players"
        prompt = PromptSettings.generate_prompt(PromptSettings.player_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_npc(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{GlobalSettings.DATA_LOCATION}/mud-images/npcs"
        prompt = PromptSettings.generate_prompt(PromptSettings.npc_tone, description)
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    async def create_monster(self, seed, description, image_name):
        image_name = self.clean_filename(image_name)
        path = f"{GlobalSettings.DATA_LOCATION}/mud-images/monsters"
        prompt = PromptSettings.monster_tone + description
        prompt = PromptSettings.generate_prompt(
            PromptSettings.monster_tone, description
        )
        return await self.generate_gemini_image(prompt, seed, path, image_name)

    def clean_filename(self, file_name):
        self.logger.debug("enter")
        file_name = file_name.replace(" ", "_")
        file_name = file_name.replace(":", "")
        file_name = file_name.replace(",", "")
        file_name = file_name.replace("!", "")
        file_name = file_name.replace("?", "")
        self.logger.debug("exit")
        return file_name

    async def generate_gemini_image(self, prompt, seed, path, name):
        try:
            prompt = json.dumps(prompt)
            self.logger.debug("enter")
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
                LogTelemetryUtility.warn("Gemini did not generate an image.")
                return None

            self.logger.debug("exit")
            return full_path

        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
            raise e

    def list_models(self):
        """Lists available Gemini models and their capabilities."""
        try:
            self.logger.debug("enter")

            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    self.logger.info(
                        f"Model Name: {m.name}, Supported Methods: {m.supported_generation_methods}"
                    )
        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
        finally:
            self.logger.debug("exit")

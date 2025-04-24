import os
import jsonpickle
from .file import AIFile
from .services.gemini import GeminiAPI
from .services.openai import OpenAIAPI
from dontcheckin import Secrets
from .services.prompt import PromptSettings
from ..enums.ai_generation_services import AIGeneration
from ..enums.images import Images
from ..events.item_image import ItemImageEvent
from ..events.monster_image import MonsterImageEvent
from ..events.npc_image import NpcImageEvent
from ..events.player_image import PlayerImageEvent
from ..events.room_image import RoomImageEvent
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
from settings.global_settings import GlobalSettings
from utilities.aws import AWSUtility


class AIImages:
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

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing AIImages() class")

        # super seed!
        self.seed = self.create_seed()

        style = GlobalSettings.IMAGE_GENERATION_SERVICE
        if style == AIGeneration.GeminiAI:
            self.generator = GeminiAPI(self.seed)
        elif style == AIGeneration.OpenAI:
            self.generator = OpenAIAPI(self.seed)

    def create_seed(self):
        self.logger.debug("enter")
        seed = 0
        for letter in enumerate("ethandrakestone + 12141999"):
            seed += ord(letter[1])
        self.logger.info(f"image seed: {seed}")
        self.logger.debug(f"exit, seed: {seed}")
        return seed

    def add_log_entry(self, log_name, file_name, description):
        self.logger.debug("enter")
        entry = AIImages.LogEntry(file_name, description).to_json()
        bytes_written = 0
        with open(log_name, "a") as text_file:
            bytes_written = text_file.write(f"{entry}\n")
        self.logger.info(f"image bytes written: {bytes_written}")
        self.logger.debug("exit")

    def read_log_entries(self, description, log_name):
        self.logger.debug("enter")
        result = None
        with open(log_name, "r") as text_file:
            contents = text_file.readlines()
            for line in contents:
                entry = AIImages.LogEntry(line)
                if entry.description == description:
                    result = entry.file_name
        self.logger.info(f"found: {True if result is not None else False}")
        self.logger.debug("exit")
        return result

    def clean_file_name(self, tone_description):
        self.logger.debug("enter")
        tone_description = ", ".join(tone_description)
        tone_description = tone_description.replace(" ", "_")
        tone_description = tone_description.replace(":", "")
        tone_description = tone_description.replace(",", "")
        tone_description = tone_description.replace("[", "")
        tone_description = tone_description.replace("]", "")
        tone_description = tone_description.replace("'", "")
        tone_description = tone_description.replace("!", "")
        tone_description = tone_description.replace("?", "")
        self.logger.debug("exit")
        return tone_description

    async def generate_image(
        self,
        item_name,
        item_description,
        player,
        world_state,
        inside=False,
        type=Images.ROOM,
    ):
        self.logger.debug("enter")

        try:
            image_name = ""
            item_description = item_description.strip()
            log_name = ""

            if type == Images.ROOM:
                log_name = self.get_data_file_name(
                    Images.ROOM, PromptSettings.room_tone
                )

                # update rooms description with weather
                if not inside:
                    item_description = world_state.weather.add_weather_description(
                        item_description
                    )

                # get already generated rooms
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Images.ITEM:
                log_name = self.get_data_file_name(
                    Images.ITEM, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Images.PLAYER:
                log_name = self.get_data_file_name(
                    Images.PLAYER, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Images.NPC:
                log_name = self.get_data_file_name(
                    Images.NPC, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == Images.MONSTER:
                log_name = self.get_data_file_name(
                    Images.MONSTER, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break

            # only generate a object if one isn't already generated
            if image_name == "":
                self.logger.info("Cannot find image for description:")
                self.logger.info(item_description)

                if type == Images.ROOM:
                    path = await self.generator.create_room(
                        self.seed, item_description, item_name
                    )
                elif type == Images.ITEM:
                    path = await self.generator.create_item(
                        self.seed, item_description, item_name
                    )
                elif type == Images.PLAYER:
                    path = await self.generator.create_player(
                        self.seed, item_description, item_name
                    )
                elif type == Images.NPC:
                    path = await self.generator.create_npc(
                        self.seed, item_description, item_name
                    )
                elif type == Images.MONSTER:
                    path = await self.generator.create_monster(
                        self.seed, item_description, item_name
                    )

                # a new image was created
                if path is None or path == "":
                    self.logger.error("Image generation failed")
                    raise Exception("Image generation failed")

                # upload s3
                s3_key = f"public/images/rooms/{item_name}"
                AWSUtility.upload_image_to_s3(
                    path,
                    s3_key,
                    make_public=True,
                    content_type="image/png",
                    logger=self.logger,
                )

                image_url = AWSUtility.generate_public_url(s3_key)
                if image_url:
                    print(f"Image uploaded successfully. Public URL: {image_url}")
                    self.add_log_entry(log_name, s3_key, item_description)
                else:
                    print("Image upload failed.")

                # send room image event
                if type == Images.ROOM:
                    await EventUtility.send_message(
                        RoomImageEvent(image_url), player.websocket
                    )
                elif type == Images.ITEM:
                    await EventUtility.send_message(
                        ItemImageEvent(image_url), player.websocket
                    )
                elif type == Images.PLAYER:
                    await EventUtility.send_message(
                        PlayerImageEvent(image_url), player.websocket
                    )
                elif type == Images.NPC:
                    await EventUtility.send_message(
                        NpcImageEvent(image_url), player.websocket
                    )
                elif type == Images.MONSTER:
                    await EventUtility.send_message(
                        MonsterImageEvent(image_url), player.websocket
                    )

            else:
                self.logger.info("Image already exists:")
                self.logger.info(image_name)
                image_url = AWSUtility.generate_public_url(image_name)
                if type == Images.ROOM:
                    await EventUtility.send_message(
                        RoomImageEvent(image_url), player.websocket
                    )
                elif type == Images.ITEM:
                    await EventUtility.send_message(
                        ItemImageEvent(image_url), player.websocket
                    )
                elif type == Images.PLAYER:
                    await EventUtility.send_message(
                        PlayerImageEvent(image_url), player.websocket
                    )
                elif type == Images.NPC:
                    await EventUtility.send_message(
                        NpcImageEvent(image_url), player.websocket
                    )
                elif type == Images.MONSTER:
                    await EventUtility.send_message(
                        MonsterImageEvent(image_url), player.websocket
                    )

        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")

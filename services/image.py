import os
import jsonpickle
from dontcheckin import Secrets
from core.enums.images import ImageEnum
from core.events.item_image import ItemImageEvent
from core.events.monster_image import MonsterImageEvent
from core.events.npc_image import NpcImageEvent
from core.events.player_image import PlayerImageEvent
from core.events.room_image import RoomImageEvent
from enums.ai_generation_services import AIGeneration
from services.ai.file import AIFile
from services.ai.services.gemini import GeminiAPI
from services.ai.services.openai import OpenAIAPI
from services.ai.services.prompt import PromptSettings
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
from settings.global_settings import GlobalSettings
from utilities.aws import AWSUtility


class ImageService:
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

    def __init__(self, world_service) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing ImageService() class")
        self.world_service = world_service

        # super seed!
        self.seed = self.create_seed()

        style = GlobalSettings.IMAGE_GENERATION_TECHNOLOGY
        if style == AIGeneration.GeminiAI:
            self.generator = GeminiAPI(self.seed)
        elif style == AIGeneration.OpenAI:
            self.generator = OpenAIAPI(self.seed)

    def create_seed(self):
        self.logger.debug("enter")
        seed = 0
        for letter in enumerate(Secrets.AI_IMAGE_SEED):
            seed += ord(letter[1])
        self.logger.info(f"image seed: {seed}")
        self.logger.debug(f"exit, seed: {seed}")
        return seed

    def add_log_entry(self, log_name, file_name, description):
        self.logger.debug("enter")
        entry = ImageService.LogEntry(file_name, description).to_json()
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
                entry = ImageService.LogEntry(line)
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
        inside=False,
        type=ImageEnum.ROOM,
    ):
        self.logger.debug("enter")

        try:
            image_name = ""
            item_description = item_description.strip()
            log_name = ""

            if type == ImageEnum.ROOM:
                log_name = self.get_data_file_name(
                    ImageEnum.ROOM, PromptSettings.room_tone
                )

                # update rooms description with weather
                if not inside:
                    item_description = self.world_service.weather.add_weather_description(
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
            elif type == ImageEnum.ITEM:
                log_name = self.get_data_file_name(
                    ImageEnum.ITEM, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == ImageEnum.PLAYER:
                log_name = self.get_data_file_name(
                    ImageEnum.PLAYER, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == ImageEnum.NPC:
                log_name = self.get_data_file_name(
                    ImageEnum.NPC, PromptSettings.player_tone
                )
                if os.path.exists(log_name):
                    with open(log_name, "r") as text_file:
                        contents = text_file.readlines()
                        for line in contents:
                            item = AIFile(line)
                            if item.description.strip() == item_description:
                                image_name = item.file_name
                                break
            elif type == ImageEnum.MONSTER:
                log_name = self.get_data_file_name(
                    ImageEnum.MONSTER, PromptSettings.player_tone
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

                if type == ImageEnum.ROOM:
                    path = await self.generator.create_room(
                        self.seed, item_description, item_name
                    )
                elif type == ImageEnum.ITEM:
                    path = await self.generator.create_item(
                        self.seed, item_description, item_name
                    )
                elif type == ImageEnum.PLAYER:
                    path = await self.generator.create_player(
                        self.seed, item_description, item_name
                    )
                elif type == ImageEnum.NPC:
                    path = await self.generator.create_npc(
                        self.seed, item_description, item_name
                    )
                elif type == ImageEnum.MONSTER:
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
                if type == ImageEnum.ROOM:
                    await RoomImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.ITEM:
                    await ItemImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.PLAYER:
                    await PlayerImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.NPC:
                    await NpcImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.MONSTER:
                    await MonsterImageEvent(image_url).send(player.websocket)

            else:
                self.logger.info("Image already exists:")
                self.logger.info(image_name)
                image_url = AWSUtility.generate_public_url(image_name)
                if type == ImageEnum.ROOM:
                    await RoomImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.ITEM:
                    await ItemImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.PLAYER:
                    await PlayerImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.NPC:
                    await NpcImageEvent(image_url).send(player.websocket)
                elif type == ImageEnum.MONSTER:
                    await MonsterImageEvent(image_url).send(player.websocket)

        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")

    def get_data_file_name(self, image_type, tone):
        self.logger.debug("enter")

        file_name = ""
        if image_type == ImageEnum.ROOM:
            file_name = f"{GlobalSettings.DATA_PATH}/rooms.txt"
        elif image_type == ImageEnum.ITEM:
            file_name = f"{GlobalSettings.DATA_PATH}/items.txt"
        elif image_type == ImageEnum.PLAYER:
            file_name = f"{GlobalSettings.DATA_PATH}/players.txt"
        elif image_type == ImageEnum.NPC:
            file_name = f"{GlobalSettings.DATA_PATH}/npcs.txt"
        elif image_type == ImageEnum.MONSTER:
            file_name = f"{GlobalSettings.DATA_PATH}/monsters.txt"

        self.logger.debug("exit")
        return file_name
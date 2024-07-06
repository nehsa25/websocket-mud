import inspect
from directions.direction import Directions
from environments.townsmee import TownSmee
from log_utils import LogUtils
from monster import Monster
from npc import Npc
from room import Room
from utility import Utility


class Environments(Utility):
        
    class Rooms(Utility):
        environment = None

        def __init__(self, logger) -> None:
            self.logger = logger
            LogUtils.debug(f"Initializing Environments.Rooms() class", self.logger)

        def add_room(
            self,
            id,
            name,
            inside,
            description,
            exits,
            environment,
            scariness,
            in_town=False,
            items=[],
            hidden_items=[],
            monsters=[],
            players=[],
            npcs=[],
        ):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            room = Room(
                id=id,
                name=name,
                inside=inside,
                description=description,
                exits=exits,
                environment=environment,
                scariness=scariness,
                items=items,
                in_town=in_town,
                hidden_items=hidden_items,
                monsters=monsters,
                players=players,
                npcs=npcs,
                logger=self.logger
            )
            LogUtils.debug(f"{method_name}: generated room: {room}", self.logger)
            return room
    npcs = None
    monster = None
    running_image_threads = []
    running_map_threads = []
    logger = None
    townsmee = None
    all_rooms = []
    all_npcs = []
    dirs = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Environments() class", self.logger)

        self.dirs = Directions(self.logger)

        if self.npcs is None:
            self.npcs = Npc(self.logger)

        if self.monster is None:
            self.monster = Monster(self.logger)

        if self.townsmee is None:
            self.townsmee = TownSmee(self.dirs, self.logger)
            self.all_rooms.extend(self.townsmee.rooms)

        # add in npcs
        LogUtils.info(
            f"{method_name}: The world has {len(self.all_rooms)} rooms", self.logger
        )



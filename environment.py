from copy import deepcopy
import inspect
import time
from directions.direction import Directions
from environments.beach import Beach
from environments.breach import Breach
from environments.forest import Forest
from environments.graveyard import Graveyard
from environments.jungle import Jungle
from environments.townsmee import TownSmee
from environments.university import University
from log_utils import LogUtils
from monster import Monster
from npc import Npc
from room import Room
from utility import Utility


class Environments(Utility):
    class RoomHistory:
        room_id: int = None
        player_name: str
        message: str
        creation_time = None
        response_time = None
        players_in_room = []
        npcs_in_room = []
        monsters_in_room = []

        def __init__(self, room_id, player_name, message, world_state):
            self.room_id = room_id
            self.player_name = player_name
            self.message = message
            room = world_state.get_room(room_id)
            self.players_in_room = room.players
            self.npcs_in_room = room.npcs
            self.monsters_in_room = room.monsters
            self.creation_time = time.time()

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
                logger=self.logger,
            )
            LogUtils.debug(f"{method_name}: generated room: {room}", self.logger)
            return room

    npcs = None
    monster = None
    running_image_threads = []
    running_map_threads = []
    logger = None

    # environments
    townsmee = None
    jungle = None
    breach = None
    forest = None
    university = None
    beach = None
    graveyard = None

    rooms = []
    all_npcs = []
    all_monsters = [] # used in world_state.py check_monster_events
    dirs = None
    room_history = []

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
            self.townsmee = TownSmee(self.logger)

        if self.jungle is None:
            self.jungle = Jungle(self.logger)

        if self.graveyard is None:
            self.graveyard = Graveyard(self.logger)

        if self.forest is None:
            self.forest = Forest(self.logger)

        if self.breach is None:
            self.breach = Breach(self.logger)

        if self.beach is None:
            self.beach = Beach(self.logger)

        if self.university is None:
            self.university = University(self.logger)

        self.rooms = [
            self.townsmee.townsquare.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_west1,
                    },
                    {
                        "direction": self.dirs.northeast,
                        "id": self.townsmee.talentroad_ne1,
                    },
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.mindroad_se1,
                    },
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.mindroad_nw1,
                    },
                    {
                        "direction": self.dirs.southwest,
                        "id": self.townsmee.talentroad_sw1,
                    },
                    {"direction": self.dirs.east, "id": self.townsmee.moonroad_east1},
                    {"direction": self.dirs.north, "id": self.townsmee.sunroad_north1},
                    {"direction": self.dirs.south, "id": self.townsmee.sunroad_south1},
                    {"direction": self.dirs.up, "id": self.townsmee.rooftop_townsquare},
                ]
            ),
            self.townsmee.inn.set_exits(
                [
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.moonroad_west2,
                    },
                    {"direction": self.dirs.up, "id": self.townsmee.inn_second},
                ]
            ),
            self.townsmee.sheriff.set_exits(
                [
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.sunroad_north1,
                    },
                ]
            ),
            self.townsmee.inn_second.set_exits(
                [
                    {"direction": self.dirs.up, "id": self.townsmee.inn_third},
                    {"direction": self.dirs.down, "id": self.townsmee.inn},
                ]
            ),
            self.townsmee.inn_third.set_exits(
                [
                    {"direction": self.dirs.down, "id": self.townsmee.inn_second},
                ]
            ),
            self.townsmee.blacksmith.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.sunroad_north1,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.blacksmith_backroom,
                    },
                ]
            ),
            self.townsmee.blacksmith_backroom.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.townsmee.blacksmith},
                ]
            ),
            self.townsmee.market.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.moonroad_east1,
                    },
                ]
            ),
            self.townsmee.armoury.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.moonroad_west1,
                    },
                ]
            ),
            self.townsmee.moonroad_west1.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_west2,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.armoury,
                    },
                ]
            ),
            self.townsmee.moonroad_east3.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_east2,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_east5,
                    },
                ]
            ),
            self.townsmee.sunroad_north1.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.sheriff,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.blacksmith,
                    },
                    {"direction": self.dirs.north, "id": self.townsmee.sunroad_north2},
                    {"direction": self.dirs.south, "id": self.townsmee.townsquare},
                ]
            ),
            self.townsmee.sunroad_north2.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_north5,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_north1,
                    }
                ]
            ),
            self.townsmee.sunroad_south1.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_south2,
                    },
                ]
            ),
            self.townsmee.sunroad_south2.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.sunroad_south1,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_south3,
                    },
                ]
            ),
            self.townsmee.sunroad_south3.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.sunroad_south2,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_south4,
                    },
                ]
            ),
            self.townsmee.sunroad_south4.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.sunroad_south3,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_south5,
                    },
                ]
            ),
            self.townsmee.sunroad_south5.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.sunroad_south4,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_south5
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.gallows_east1,
                    },
                ]
            ),
            self.townsmee.gallows_east1.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.townsmee.sunroad_south5},
                    {"direction": self.dirs.east, "id": self.townsmee.gallows_east2},
                ]
            ),
            self.townsmee.gallows_east2.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.townsmee.gallows_east1},
                    {"direction": self.dirs.east, "id": self.townsmee.gallows_east3},
                ]
            ),
            self.townsmee.gallows_east3.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.townsmee.gallows_east2},
                    {"direction": self.dirs.south, "id": self.townsmee.gallows},
                ]
            ),
            self.townsmee.gallows.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.gallows_east3,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.lower_quarter,
                    },
                ]
            ),
            self.townsmee.lower_quarter.set_exits(
                [
                    {"direction": self.dirs.north, "id": self.townsmee.gallows},
                ]
            ),
            self.townsmee.mindroad_nw1.set_exits(
                [
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.mindroad_nw2,
                    },
                ]
            ),
            self.townsmee.mindroad_se1.set_exits(
                [
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.mindroad_se2,
                    },
                ]
            ),
            self.townsmee.talentroad_ne1.set_exits(
                [
                    {
                        "direction": self.dirs.southwest,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.talentroad_ne2,
                    },
                ]
            ),
            self.townsmee.talentroad_sw1.set_exits(
                [
                    {
                        "direction": self.dirs.northeast,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.southwest,
                        "id": self.townsmee.talentroad_sw2,
                    },
                ]
            ),
            self.townsmee.talentroad_sw2.set_exits(
                [
                    {
                        "direction": self.dirs.northeast,
                        "id": self.townsmee.talentroad_sw1,
                    },
                    {
                        "direction": self.dirs.southwest,
                        "id": self.townsmee.talentroad_sw3,
                    },
                ]
            ),
            self.townsmee.mindroad_se3.set_exits(
                [
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.mindroad_bridge,
                    },
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.mindroad_se2,
                    },
                ]
            ),
            self.townsmee.mindroad_se2.set_exits(
                [
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.mindroad_se1,
                    },
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.mindroad_se3,
                    },
                ]
            ),
            self.townsmee.mindroad_bridge.set_exits(
                [
                    {
                        "direction": self.dirs.northwest,
                        "id": self.townsmee.mindroad_se3,
                    },
                    {
                        "direction": self.dirs.southeast,
                        "id": self.university.university_entry,
                    },
                ]
            ),
            self.jungle.jungle_entry.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.townsmee.outer_east5},
                ]
            ),
            self.university.university_entry.set_exits(
                [
                    {"direction": self.dirs.northwest, "id": self.townsmee.mindroad_bridge},
                    {"direction": self.dirs.east, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_courtyard.set_exits(
                [
                    {"direction": self.dirs.northeast, "id": self.university.university_garden},
                    {"direction": self.dirs.west, "id": self.university.university_entry},
                    {"direction": self.dirs.north, "id": self.university.university_scriptorium},
                    {"direction": self.dirs.east, "id": self.university.university_dormitory},
                    {"direction": self.dirs.south, "id": self.university.university_refectory},
                    {"direction": self.dirs.southwest, "id": self.university.university_observatory},
                    {"direction": self.dirs.northwest, "id": self.university.university_mirrology}  
                ]
            ),   
            self.university.university_scriptorium.set_exits(
                [
                    {"direction": self.dirs.south, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_garden.set_exits(
                [
                    {"direction": self.dirs.southwest, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_dormitory.set_exits(
                [
                    {"direction": self.dirs.west, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_refectory.set_exits(
                [
                    {"direction": self.dirs.north, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_observatory.set_exits(
                [
                    {"direction": self.dirs.northeast, "id": self.university.university_courtyard},
                ]
            ),
            self.university.university_mirrology.set_exits(
                [
                    {"direction": self.dirs.southeast, "id": self.university.university_courtyard},
                ]
            ),    
            self.forest.forest_entry.set_exits(
                [
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_north5,
                    },
                ]
            ),
            self.beach.beach_entry.set_exits(
                [
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_west5,
                    },
                ]
            ),
            self.breach.breach_portal.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_south5,
                    },
                ]
            ),
            self.townsmee.outer_west5.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west4,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.beach.beach_entry,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.moonroad_west3,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west6,
                    },
                ]
            ),
            self.townsmee.outer_west6.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west5,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west7,
                    },
                ]
            ),
            self.townsmee.outer_west7.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west6,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west8,
                    },
                ]
            ),
            self.townsmee.outer_west8.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west7,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west9,
                    },
                ]
            ),
            self.townsmee.outer_west9.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west8,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west10,
                    },
                ]
            ),
            self.townsmee.outer_west10.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west9,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_south1,
                    },
                ]
            ),
            self.townsmee.outer_south1.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west10,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south2,
                    },
                ]
            ),
            self.townsmee.outer_south2.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south1,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south3,
                    },
                ]
            ),
            self.townsmee.outer_south3.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south2,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south4,
                    },
                ]
            ),
            self.townsmee.outer_south4.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south3,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south5,
                    },
                ]
            ),
            self.townsmee.outer_south5.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south4,
                    },
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.sunroad_south5,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.breach.breach_portal,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south6,
                    },
                ]
            ),
            self.townsmee.outer_south6.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south5,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south7,
                    },
                ]
            ),
            self.townsmee.outer_south7.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south6,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south8,
                    },
                ]
            ),
            self.townsmee.outer_south8.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south7,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south9,
                    },
                ]
            ),
            self.townsmee.outer_south9.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south8,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_south10,
                    },
                ]
            ),
            self.townsmee.outer_south10.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_south9,
                    },
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east10,
                    },
                ]
            ),
            self.townsmee.outer_east10.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east9,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_south10,
                    },
                ]
            ),
            self.townsmee.outer_east9.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east8,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east10,
                    },
                ]
            ),
            self.townsmee.outer_east8.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east7,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east9,
                    },
                ]
            ),
            self.townsmee.outer_east7.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east6,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east8,
                    },
                ]
            ),
            self.townsmee.outer_east6.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east5,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east7,
                    },
                ]
            ),
            self.townsmee.outer_east5.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east4,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_east3,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.jungle.jungle_entry,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east6,
                    },
                ]
            ),
            self.townsmee.outer_east4.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east3,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east5,
                    },
                ]
            ),
            self.townsmee.outer_east3.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east2,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east4,
                    },
                ]
            ),
            self.townsmee.outer_east2.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_east1,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east3,
                    },
                ]
            ),
            self.townsmee.outer_east1.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_north10,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east2,
                    },
                ]
            ),
            self.townsmee.outer_north10.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north9,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_east1,
                    },
                ]
            ),
            self.townsmee.outer_north9.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north8,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north10,
                    },
                ]
            ),
            self.townsmee.outer_north8.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north7,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north9,
                    },
                ]
            ),
            self.townsmee.outer_north7.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north6,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north8,
                    },
                ]
            ),
            self.townsmee.outer_north6.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north5,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north7,
                    },
                ]
            ),
            self.townsmee.outer_north5.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north4,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.sunroad_north2,
                    },
                    {
                        "direction": self.dirs.north,
                        "id": self.forest.forest_entry,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north6,
                    },
                ]
            ),
            self.townsmee.outer_north4.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north3,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north5,
                    },
                ]
            ),
            self.townsmee.outer_north3.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north2,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north4,
                    },
                ]
            ),
            self.townsmee.outer_north2.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_north1,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north3,
                    },
                ]
            ),
            self.townsmee.outer_north1.set_exits(
                [
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west1,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.outer_north2,
                    },
                ]
            ),
            self.townsmee.outer_west1.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_north1,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west2,
                    },
                ]
            ),
            self.townsmee.outer_west2.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west1,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west3,
                    },
                ]
            ),
            self.townsmee.outer_west3.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west2,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west4,
                    },
                ]
            ),
            self.townsmee.outer_west4.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.outer_west3,
                    },
                    {
                        "direction": self.dirs.south,
                        "id": self.townsmee.outer_west5,
                    },
                ]
            ),
            self.townsmee.moonroad_west3.set_exits(
                [
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.moonroad_west2,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.outer_west5,
                    },
                ]
            ),
            self.townsmee.moonroad_west2.set_exits(
                [
                    {
                        "direction": self.dirs.north,
                        "id": self.townsmee.inn,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.moonroad_west1,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_west3,
                    },
                ]
            ),
            self.townsmee.moonroad_east1.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.townsquare,
                    },
                    {"direction": self.dirs.east, "id": self.townsmee.moonroad_east2},
                    {"direction": self.dirs.south, "id": self.townsmee.market},
                ]
            ),
            self.townsmee.moonroad_east2.set_exits(
                [
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.moonroad_east3,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.moonroad_east1,
                    },
                ]
            ),
            self.townsmee.talentroad_ne2.set_exits(
                [
                    {
                        "direction": self.dirs.southwest,
                        "id": self.townsmee.talentroad_ne1,
                    },
                ]
            ),
            self.townsmee.talentroad_sw3.set_exits(
                [
                    {
                        "direction": self.dirs.northeast,
                        "id": self.townsmee.talentroad_sw2,
                    },
                ]
            ),
            self.townsmee.mindroad_nw2.set_exits(
                [
                    {
                        "direction": self.dirs.southeast,
                        "id": self.townsmee.mindroad_nw1,
                    },
                ]
            ),
            self.townsmee.rooftop_townsquare.set_exits(
                [
                    {
                        "direction": self.dirs.down,
                        "id": self.townsmee.townsquare,
                    },
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.rooftop_west1,
                    },
                ]
            ),
            self.townsmee.rooftop_west1.set_exits(
                [
                    {
                        "direction": self.dirs.west,
                        "id": self.townsmee.rooftop_west2,
                    },
                    {
                        "direction": self.dirs.down,
                        "id": self.townsmee.moonroad_west1,
                    },
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.rooftop_townsquare,
                    },
                ]
            ),
            self.townsmee.rooftop_west2.set_exits(
                [
                    {
                        "direction": self.dirs.east,
                        "id": self.townsmee.rooftop_west1,
                    },
                    {
                        "direction": self.dirs.down,
                        "id": self.townsmee.moonroad_west2,
                    },
                ]
            ),
        ]

        # add in npcs
        LogUtils.info(
            f"{method_name}: The world has {len(self.rooms)} rooms",
            self.townsmee.logger,
        )

    async def update_room_history(self, room_id, player_name, message, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.townsmee.logger)
        room_histories = []
        histories = deepcopy(self.townsmee.room_history)
        last_history = None
        for history in histories:
            if room_id == history.room_id:
                last_history.response_time = time.time()
                room_histories.append(last_history)
            else:
                room_histories.append(
                    self.townsmee.append_room_history(
                        room_id, player_name, message, world_state
                    )
                )

        room_histories.append(history)
        LogUtils.debug(f"{method_name}: exit", self.townsmee.logger)
        self.townsmee.room_history = deepcopy(room_histories)

    async def append_room_history(self, room_id, player_name, message, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(
            f"{method_name}: enter, message: {message}", self.townsmee.logger
        )
        room_history_message = self.townsmee.RoomHistory(
            room_id, player_name, message, world_state
        )
        self.townsmee.room_history.append(room_history_message)
        LogUtils.debug(f"{method_name}: exit", self.townsmee.logger)

    async def get_room_history(self, room_id):
        lines = [a for a in self.townsmee.room_history if a.id == room_id]
        return lines

    async def get_room_by_name(self, name):
        room = None
        rooms = [a for a in self.rooms if a.name == name]
        if len(rooms) > 0:
            room = rooms[0]
        else:
            raise Exception(f"Room not found: {name}")
        return room
        
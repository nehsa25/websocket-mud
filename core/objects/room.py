# from copy import deepcopy
# import random
# from core.enums.room_danger_levels import RoomDangerEnum
# from utilities.log_telemetry import LogTelemetryUtility


# class Room:
#     class BasicRoom:
#         class BasicExit:
#             name = ""
#             description = ""

#             def __init__(self, exit) -> None:
#                 self.name = exit.name
#                 self.description = exit.description

#         class BasicMob:
#             name = ""
#             alignment = ""
#             description = ""

#             def __init__(self, name, alignment, description) -> None:
#                 self.name = name
#                 self.alignment = alignment
#                 self.description = description

#         class BasicItem:
#             name = ""
#             description = ""

#             def __init__(self, name, description) -> None:
#                 self.name = name
#                 self.description = description

#         name = ""
#         description = ""
#         monsters = []
#         items = []
#         npcs = []
#         players = []
#         exits = []

#         def __init__(self, room):
#             self.name = room.name
#             self.description = room.description

#             for exit in room.exits:
#                 self.exits.append(self.BasicExit(exit))
#             self.exits = self.exits

#             for monster in room.monsters:
#                 self.monsters.append(
#                     self.BasicMob(monster.name, monster.alignment, monster.description)
#                 )
#             self.monsters = self.monsters

#             for item in room.items:
#                 self.items.append(self.BasicItem(item.name, item.description))
#             self.items = self.items

#             for npc in room.npcs:
#                 self.npcs.append(
#                     self.BasicMob(npc.name, npc.alignment, npc.description)
#                 )
#             self.npcs = self.npcs

#             for player in room.players:
#                 self.players.append(
#                     self.BasicMob(player.name, player.alignment, player.description)
#                 )
#             self.players = self.players

#     name = ""
#     inside = False
#     description = ""
#     monster_spawn = False
#     monster_saturation = 0.7
#     scariness = 0
#     environment = (None,)
#     history = []
#     exits = ([],)
#     items = ([],)
#     hidden_items = ([],)
#     monsters = ([],)
#     players = ([],)  # you, hopefully
#     npcs = []  # actual instances of npcs
#     npc_types = []  # this is the enum of the types of npcs that can be in the room
#     in_town = False
#     logger = None

#     def __init__(
#         self,
#         name,
#         inside,
#         description,
#         environment,
#         scariness=None,
#         items=[],
#         hidden_items=[],
#         monsters=[],
#         players=[],
#         npcs=[],
#         npc_types=[],
#         in_town=False,
#     ) -> None:
#         self.name = name
#         self.inside = inside
#         self.description = description
#         self.environment = environment
#         self.items = items
#         self.scariness = scariness
#         self.hidden_items = hidden_items
#         self.monsters = monsters
#         self.players = players
#         self.npcs = npcs
#         self.in_town = in_town
#         self.npc_types = npc_types
#         self.logger = LogTelemetryUtility.get_logger(__name__)
#         self.scariness = random.choice(list(RoomDangerEnum)).value
#         self.logger.debug("Initializing Room() class")

#     def set_exits(self, exits):
#         self.exits = exits
#         return deepcopy(self)

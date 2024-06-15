from breach import Breach
from forest import Forest
from jungle import Jungle
from log_utils import LogUtils
from townsmee import TownSmee

class Rooms: 
    logger = None
    # forest = Forest()
    # breach = Breach()
    # jungle = Jungle()
    townsmee = None
    envionments = []
    world_name = ""
    
    def __init__(self, world_name, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Rooms() class", self.logger)
        self.world_name = world_name
        if (self.townsmee is None):
            self.townsmee = TownSmee(self.world_name, self.logger)
            self.envionments.append(self.townsmee)

    def get_rooms(self):
        rooms = []
        for env in self.envionments:
            rooms.extend(env.rooms)
        return rooms
        
        # self.all_rooms.extend(self.forest.rooms)
        # self.all_rooms.extend(self.breach.rooms)
        # self.all_rooms.extend(self.jungle.rooms)


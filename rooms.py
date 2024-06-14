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
    all_rooms = []
    
    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Rooms() class", self.logger)
        self.townsmee = TownSmee(self.logger)
        # self.all_rooms.extend(self.forest.rooms)
        # self.all_rooms.extend(self.breach.rooms)
        # self.all_rooms.extend(self.jungle.rooms)
        self.all_rooms.extend(self.townsmee.rooms)

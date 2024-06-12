from breach import Breach
from forest import Forest
from jungle import Jungle
from townsmee import TownSmee

class Rooms:    
    forest = Forest()
    breach = Breach()
    jungle = Jungle()
    townsmee = TownSmee()    
    all_rooms = []
    
    def __init__(self) -> None:
        self.all_rooms.extend(self.forest.rooms)
        self.all_rooms.extend(self.breach.rooms)
        self.all_rooms.extend(self.jungle.rooms)
        self.all_rooms.extend(self.townsmee.rooms)

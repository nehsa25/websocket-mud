import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class University:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = True
    name = "Town Smee - University"
    type = Utility.EnvironmentTypes.UNIVERSITY
    
    # rooms
    university_entry = None
    university_courtyard = None
    university_garden = None
    university_scriptorium = None
    university_dormitory = None
    university_refectory = None
    university_observatory = None
    university_mirrology = None    

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing University() class", self.logger)
        self.monster_saturation = 0.5
        self.university_entry = Room(
                name=f"{self.name} - Entrance Stone Arches",
                inside=False,
                description="""The entrance to the University of Smee is a grand affair. Two stone arches, each carved with intricate depictions of Wizard Renkath and the founder of the University. Ethereal crimson light streams through the depictions.""",
                environment=self.type,
                logger=logger
            )
        
        self.university_courtyard = Room(
                name=f"{self.name} - Courtyard",
                inside=False,
                description="""The university of Smee, simply called “The University” is a sprawling complex of buildings, courtyards, and gardens. The buildings are made of a white stone that seems to glow unnaturally in the sunlight. The University is a place of learning, research, and there’s a sense of tranquility not found elsewhere in the city. The air is filled with the sounds of students and teachers going about their business.
<br><br>
A sign reads:<br>
-	Garden: Northeast<br>
-	Scriptorium: North<br>
-	Dormitory: East<br>
-	Refectory: South<br>
-	Observatory: Southwest<br>
-	Mirrology: Northwest<br>
-	Town Smee: West<br><br>
""",
                environment=self.type,
                logger=logger
            )
        
        self.university_garden = Room(
                name=f"{self.name} - Garden",
                inside=False,
                description="""The garden of the university is breath taking. Flowers, herbs, and trees of every shape and color imaginable are planted in precise rows. The air is filled with the sounds of bees and birds.""",
                environment=self.type,
                npc_types=[Utility.Npcs.GARDENER],
                logger=logger
            )
        
        self.university_scriptorium = Room(
                name=f"{self.name} - Scriptorium",
                inside=True,
                description="""The entire perimeter of the room is lined with scrolls and books. The center of the room has desks arranged with paper and quills ready.""",
                environment=self.type,
                logger=logger
            )
        
        self.university_dormitory = Room(
                name=f"{self.name} - Dormitory",
                inside=True,
                description="""The dormitory is a single large room with rows of beds. Each bed has a chest at the foot of it with a small lock securing it shut.""",
                environment=self.type,
                logger=logger
            )
        
        self.university_refectory = Room(
                name=f"{self.name} - Refectory",
                inside=True,
                description="""The sign above the refectory reads "Come, Refresh." Inside the refectory, there are long benches where meals are eaten together. The smell of food lingers in the air despite no food being served right now. The kitchen is at the back of the room.""",
                environment=self.type,
                logger=logger
            )
        
        self.university_observatory = Room(
                name=f"{self.name} - Observatory",
                inside=True,
                description="""The largest telescope you've ever seen lies in the center of the room. The room is dark.""",
                environment=self.type,
                logger=logger
            )
        
        self.university_mirrology = Room(
                name=f"{self.name} - Mirrology",
                inside=True,
                description="""The mirrology room is filled with magical mirrors of all shapes and sizes. Every mirror has moving images within it.""",
                environment=self.type,
                npc_types=[Utility.Npcs.WIZARD],
                logger=logger
            )

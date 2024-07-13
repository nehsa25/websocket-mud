import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class TownSmee:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = True
    name = "Town Smee"
    type = Utility.Share.EnvironmentTypes.TOWNSMEE

    # rooms
    townsquare = None
    inn = None
    inn_second = None
    inn_third = None
    blacksmith = None
    blacksmith_backroom = None
    market = None
    armoury = None
    moonroad_west1 = None
    moonroad_east3 = None
    sunroad_north1 = None
    sunroad_south1 = None
    sunroad_south2 = None
    sunroad_south3 = None
    sunroad_south4 = None
    gallows_east1 = None
    gallows_east2 = None
    gallows = None
    lower_quarter = None
    mindroad_nw1 = None
    mindroad_se1 = None
    talentroad_ne1 = None
    talentroad_sw1 = None
    talentroad_sw2 = None
    mindroad_se2 = None
    mindroad_bridge = None
    mindroad_se3 = None
    talentroad_sw3 = None
    talentroad_ne2 = None
    mindroad_nw2 = None
    gallows_east2 = None
    gallows_east3 = None
    sunroad_south5 = None
    sunroad_north2 = None
    moonroad_east2 = None
    moonroad_west2 = None
    moonroad_west3 = None
    rooftop_townsquare = None
    rooftop_west1 = None
    rooftop_west2 = None
    outer_west1 = None
    outer_west2 = None
    outer_west3 = None
    outer_west4 = None
    outer_west5 = None
    outer_west6 = None
    outer_west7 = None
    outer_west8 = None
    outer_west9 = None
    outer_west10 = None
    outer_south1 = None
    outer_south2 = None
    outer_south3 = None
    outer_south4 = None
    outer_south5 = None
    outer_south6 = None
    outer_south7 = None
    outer_south8 = None
    outer_south9 = None
    outer_south10 = None
    outer_east1 = None
    outer_east2 = None
    outer_east3 = None
    outer_east4 = None
    outer_east5 = None
    outer_east6 = None
    outer_east7 = None
    outer_east8 = None
    outer_east9 = None
    outer_east10 = None
    outer_north1 = None
    outer_north2 = None
    outer_north3 = None
    outer_north4 = None
    outer_north5 = None
    outer_north6 = None
    outer_north7 = None
    outer_north8 = None
    outer_north9 = None
    outer_north10 = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing TownSmee() class", self.logger)
        self.monster_saturation = 0.5

        self.townsquare = Room(
            name=f"{self.name} - Town Square",
            inside=False,
            description="You are in the town square of the Town of Smee. It's a large open cobblestone area with a bronze water fountain. The fountain is in the shape of a large, ferocious dire wolf. Water jets from the foutain mouth in a small arc. There's a festive feeling to the area and people and wagons move with purpose in all directions.",
            items=[Items.helmet, Items.stick, Items.maul],
            monsters=[],
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            environment=self.type,
            logger=logger,
        )
        self.inn = Room(
            name=f"{self.name} - Inn",
            inside=True,
            description="You find yourself within a majestic inn. A worn, well-kept fireplace burned softly in the corner. There's a shelf with a small assortment of books and a prized map of the town and surrounding area stands on display but it is sealed behind glass to prevent touching.",
            npc_types=[Utility.Share.Npcs.INNKEEPER, Utility.Share.Npcs.PRINCESS],
            environment=self.type,
            logger=logger,
        )
        self.sheriff = Room(
            name=f"{self.name} - Sheriff's Office",
            inside=True,
            description="You are in the sheriff's office. A locked cell is in the corner of the Room. Currently, it is empty. A young bestraught woman is pleading and gusticulating to someone behind a small window.",
            npc_types=[Utility.Share.Npcs.SHERIFF],
            environment=self.type,
            logger=logger,
        )
        self.inn_second = Room(
            name=f"{self.name} - Inn, second floor",
            inside=True,
            description="You are on the second floor of the inn. Rooms line the hallway.",
            environment=self.type,
            logger=logger,
        )
        self.inn_third = Room(
            name=f"{self.name} - Inn, third floor",
            inside=True,
            description="You are on the third floor of the inn. Rooms line the hallway. A beautiful vase with daisies sit on a table in broad view.",
            hidden_items=[Items.helmet],
            environment=self.type,
            logger=logger,
        )
        self.blacksmith = Room(
            name=f"{self.name} - Blacksmith",
            inside=True,
            npc_types=[Utility.Share.Npcs.BLACKSMITH],
            description="You are in the blacksmith's shop. An assortment of the blacksmiths wares are on display.",
            environment=self.type,
            logger=logger,
        )
        self.blacksmith_backroom = Room(
            name=f"{self.name} - Blacksmith, back room",
            inside=True,
            description="You are in the blacksmith's back Room. A hot forge still burns smoldering coals.",
            environment=self.type,
            logger=logger,
        )
        self.market = Room(
            name=f"{self.name} - Market",
            inside=False,
            description="You are in the farmers market. Smells of exotic spices and searing meats are everywhere and loud vendors yell out their wares. The market is bustling with activity. Children and dogs are seen running everywhere with bright smiles. You even spot a Rite, a small azure and beige colored lizard two feet tall. Rites are harmless joyful creatures.",
            npc_types=[Utility.Share.Npcs.MERCHANT, Utility.Share.Npcs.THIEF],
            environment=self.type,
            logger=logger,
        )
        self.armoury = Room(
            name=f"{self.name} - Armoury",
            inside=True,
            description="You are in the town armoury. A prominent case displays a beautifully crafted broadsword. The blade of the sword seems to glow slightly. It has a worn but well-kepted tightly-bound leather hilt. An assortment of other swords, shields, and armor are on display along the walls.",
            npc_types=[Utility.Share.Npcs.ARMORER],
            environment=self.type,
            logger=logger,
        )
        self.moonroad_west1 = Room(
            name=f"{self.name} - Moon Road (West)---1",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.moonroad_east3 = Room(
            name=f"{self.name} - Moon Road (East)---3",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_north1 = Room(
            name=f"{self.name} - Sun Road (North)---1",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_south1 = Room(
            name=f"{self.name} - Sun Road (South)---1",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_south2 = Room(
            name=f"{self.name} - Sun Road (South)---2",
            inside=False,
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_south3 = Room(
            name=f"{self.name} - Sun Road (South)---3",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_south4 = Room(
            name=f"{self.name} - Sun Road (South)---4",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.gallows_east1 = Room(
            name=f"{self.name} - Gallows Road (East)---1",
            inside=False,
            description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            environment=self.type,
            logger=logger,
        )
        self.gallows_east2 = Room(
            name=f"{self.name} - Gallows Road (East)---2",
            inside=False,
            description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
            environment=self.type,
            logger=logger,
        )
        self.gallows = Room(
            name=f"{self.name} - The Gallows",
            inside=False,
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            description=f"The road widens into a large gathering area. Sets of gallow line the road. A sign reads 'Next service in 3 days'. Admission is free but donations are accepted.",
            environment=self.type,
            logger=logger,
        )
        self.lower_quarter = Room(
            name=f"{self.name} - The Lower Quarter",
            inside=False,
            description=f"A gate with two guards stands before you. Each guard casually leans against halberds taller than they are. The gate is open and the guards are pleasantly chatting with each other whilst a long line of weary towns folk await admission into the city. A sign reads “1 copper entrance free. No exceptions.”",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_nw1 = Room(
            name=f"{self.name} - Mind Road (Northwest)---1",
            inside=False,
            description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest to southeast in Smee, the road extends far to the southeast at the University of Smee.",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_se1 = Room(
            name=f"{self.name} - Mind Road (SouthEast)---1",
            inside=False,
            description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest, past the town square, to the University of Smee to the southeast.",
            environment=self.type,
            logger=logger,
        )
        self.talentroad_ne1 = Room(
            name=f"{self.name} - Talent Road (NorthEast)---1",
            inside=False,
            description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
            environment=self.type,
            logger=logger,
        )
        self.talentroad_sw1 = Room(
            name=f"{self.name} - Talent Road (SouthWest)---1",
            inside=False,
            description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
            environment=self.type,
            logger=logger,
        )
        self.talentroad_sw2 = Room(
            name=f"{self.name} - Talent Road (SouthWest)---2",
            inside=False,
            description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_se2 = Room(
            name=f"{self.name} - Mind Road (SouthEast)---2",
            inside=False,
            description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest, past the town square, to the University of Smee to the southeast.",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_bridge = Room(
            name=f"{self.name} - Mind Road (SouthEast) - Massive Bridge",
            inside=False,
            description=f"A large bridge spans a fast-flowing river.  The bridge is made from a glossy dark, almost black wood. Despite its apparently fragileness, the wood is extremely hard and no amount of weight has been found to cause the bridge to move.",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_se3 = Room(
            name=f"{self.name} - Mind Road (SouthEast)---3",
            inside=False,
            description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest, past the town square, to the University of Smee to the southeast.",
            environment=self.type,
            logger=logger,
        )
        self.talentroad_sw3 = Room(
            name=f"{self.name} - Talent Road (SouthWest)---3",
            inside=False,
            description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
            environment=self.type,
            logger=logger,
        )
        self.talentroad_ne2 = Room(
            name=f"{self.name} - Talent Road (NorthEast)---2",
            inside=False,
            description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
            environment=self.type,
            logger=logger,
        )
        self.mindroad_nw2 = Room(
            name=f"{self.name} - Mind Road (Northwest)---2",
            inside=False,
            description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest to southeast in Smee, the road extends far to the southeast at the University of Smee.",
            environment=self.type,
            logger=logger,
        )
        self.gallows_east2 = Room(
            name=f"{self.name} - Gallows Road (East)---2",
            inside=False,
            description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            environment=self.type,
            logger=logger,
        )
        self.gallows_east3 = Room(
            name=f"{self.name} - Gallows Road (East)---3",
            inside=False,
            description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
            npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
            environment=self.type,
            logger=logger,
        )
        self.sunroad_south5 = Room(
            name=f"{self.name} - Sun Road (South)---5",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.sunroad_north2 = Room(
            name=f"{self.name} - Sun Road (North)---2",
            inside=False,
            description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.moonroad_east1 = Room(
            name=f"{self.name} - Moon Road (East)---1",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.moonroad_east2 = Room(
            name=f"{self.name} - Moon Road (East)---2",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.moonroad_west2 = Room(
            name=f"{self.name} - Moon Road (West)---2",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.moonroad_west3 = Room(
            name=f"{self.name} - Moon Road (West)---3",
            inside=False,
            description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
            environment=self.type,
            logger=logger,
        )
        self.rooftop_townsquare = Room(
            name=f"{self.name} - Rooftop - Townsquare",
            inside=False,
            description=f"You are on the rooftop of the town square. The rooftop feels secure with dark, sturdy wooden shingles. You can see the entire town from here and see paths to other rooftops. The town square is bustling with activity below.",
            environment=self.type,
            logger=logger,
        )
        self.rooftop_west1 = Room(
            name=f"{self.name} - Rooftop (West)---1",
            inside=False,
            description=f"The rooftop feels secure with dark, sturdy wooden shingles. You are on the rooftop overlooking the entrance to armoury below. You may be able to get down from here but will unikely be able to get back up here.",
            environment=self.type,
            logger=logger,
        )
        self.rooftop_west2 = Room(
            name=f"{self.name} - Rooftop (West)---2",
            inside=False,
            description=f"The rooftop feels secure with dark, sturdy wooden shingles. You are on the rooftop overlooking the entrance to inn below. You may be able to get down from here but will unikely be able to get back up here.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west1 = Room(
            name=f"{self.name} - Outer wall (Inside West)---1",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west2 = Room(
            name=f"{self.name} - Outer wall (Inside West)---2",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west3 = Room(
            name=f"{self.name} - Outer wall (Inside West)---3",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west4 = Room(
            name=f"{self.name} - Outer wall (Inside West)---4",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west5 = Room(
            name=f"{self.name} - Outer wall (Inside West)---5",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west6 = Room(
            name=f"{self.name} - Outer wall (Inside West)---6",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west7 = Room(
            name=f"{self.name} - Outer wall (Inside West)---7",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_west8 = Room(
            name=f"{self.name} - Outer wall (Inside West)---8",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )

        self.outer_west9 = Room(
            name=f"{self.name} - Outer wall (Inside West)---9",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )

        self.outer_west10 = Room(
            name=f"{self.name} - Outer wall (Inside West)---10",
            inside=False,
            description=f"You are at the western edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south1 = Room(
            name=f"{self.name} - Outer wall (Inside South)---1",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south2 = Room(
            name=f"{self.name} - Outer wall (Inside South)---2",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south3 = Room(
            name=f"{self.name} - Outer wall (Inside South)---3",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south4 = Room(
            name=f"{self.name} - Outer wall (Inside South)---4",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south5 = Room(
            name=f"{self.name} - Outer wall (Inside South)---5",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south6 = Room(
            name=f"{self.name} - Outer wall (Inside South)---6",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south7 = Room(
            name=f"{self.name} - Outer wall (Inside South)---7",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south8 = Room(
            name=f"{self.name} - Outer wall (Inside South)---8",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south9 = Room(
            name=f"{self.name} - Outer wall (Inside South)---9",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_south10 = Room(
            name=f"{self.name} - Outer wall (Inside South)---10",
            inside=False,
            description=f"You are at the southern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east1 = Room(
            name=f"{self.name} - Outer wall (Inside East)---1",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east2 = Room(
            name=f"{self.name} - Outer wall (Inside East)---2",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east3 = Room(
            name=f"{self.name} - Outer wall (Inside East)---3",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east4 = Room(
            name=f"{self.name} - Outer wall (Inside East)---4",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east5 = Room(
            name=f"{self.name} - Outer wall (Inside East)---5",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east6 = Room(
            name=f"{self.name} - Outer wall (Inside East)---6",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east7 = Room(
            name=f"{self.name} - Outer wall (Inside East)---7",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east8 = Room(
            name=f"{self.name} - Outer wall (Inside East)---8",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east9 = Room(
            name=f"{self.name} - Outer wall (Inside East)---9",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_east10 = Room(
            name=f"{self.name} - Outer wall (Inside East)---10",
            inside=False,
            description=f"You are at the eastern edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north1 = Room(
            name=f"{self.name} - Outer wall (Inside North)---1",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north2 = Room(
            name=f"{self.name} - Outer wall (Inside North)---2",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north3 = Room(
            name=f"{self.name} - Outer wall (Inside North)---3",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north4 = Room(
            name=f"{self.name} - Outer wall (Inside North)---4",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north5 = Room(
            name=f"{self.name} - Outer wall (Inside North)---5",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north6 = Room(
            name=f"{self.name} - Outer wall (Inside North)---6",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north7 = Room(
            name=f"{self.name} - Outer wall (Inside North)---7",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north8 = Room(
            name=f"{self.name} - Outer wall (Inside North)---8",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north9 = Room(
            name=f"{self.name} - Outer wall (Inside North)---9",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )
        self.outer_north10 = Room(
            name=f"{self.name} - Outer wall (Inside North)---10",
            inside=False,
            description=f"You are at the norther edge of Town Smee, just inside the outer wall. A large, cobbled road runs along the entire outer wall of town, 9 meters. The wall rises 7 meters high of young green timber. It's painted fresh with glossy brown paint on the inside.",
            environment=self.type,
            logger=logger,
        )

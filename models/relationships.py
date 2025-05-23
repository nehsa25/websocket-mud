from models.db_armor import DBArmor
from models.db_characters import DBCharacter
from models.db_directions import DBDirection
from models.db_environment import DBEnvironment
from models.db_exits import DBExit
from models.db_items import DBItem
from models.db_items_food import DBFood
from models.db_items_lightsources import DBLightsource
from models.db_items_weapons import DBWeapon
from models.db_mobs import DBMob
from models.db_mobs_monsters import DBMonster
from models.db_mobs_npcs import DBNpc
from models.db_players import DBPlayer
from models.db_player_class import DBPlayerClass
from models.db_player_race import DBPlayerRace
from models.db_room import DBRoom
from models.db_effects import DBEffect
from sqlalchemy.orm import relationship

from utilities.log_telemetry import LogTelemetryUtility

def define_relationships():
    logger = LogTelemetryUtility.get_logger(__name__)
    logger.debug("Defining relationships...")

    logger.debug("...directions")
    DBDirection.opposite = relationship("DBDirection", remote_side=[DBDirection.id], 
                                        backref="reverse_direction")
    
    logger.debug("...rooms")
    DBRoom.environment = relationship("DBEnvironment", back_populates="rooms")
    DBRoom.npcs = relationship("DBNpc", back_populates="rooms")
    DBRoom.monsters = relationship("DBMonster", back_populates="rooms")
    DBRoom.items = relationship("DBItem", back_populates="rooms")
    DBRoom.characters = relationship("DBCharacter", back_populates="rooms")
    DBRoom.exits = relationship("DBExit", back_populates="rooms")  

    logger.debug("...environments")
    DBEnvironment.rooms = relationship("DBRoom", back_populates="environments")

    logger.debug("...exits")
    DBExit.room = relationship("DBRoom", back_populates="exits")

    logger.debug("...items")
    DBItem.room = relationship("DBRoom", back_populates="items")
    DBItem.food = relationship("DBFood", back_populates="items", uselist=False)
    DBItem.lightsource = relationship("DBLightsource", back_populates="items", uselist=False)
    DBItem.weapon = relationship("DBWeapon", back_populates="items", uselist=False)
    DBItem.armor = relationship("DBArmor", back_populates="items", uselist=False)
    DBItem.effects = relationship("DBEffect", secondary="item_effects", back_populates="items")

    logger.debug("...food")
    DBFood.item = relationship("DBItem", back_populates="food_items")
    DBFood.food_effects = relationship("DBFoodEffect", back_populates="food_items")

    logger.debug("...lightsources")
    DBLightsource.item = relationship("DBItem", back_populates="lightsources")

    logger.debug("...weapons")
    DBWeapon.item = relationship("DBItem", back_populates="weapons")

    logger.debug("...armor")
    DBArmor.item = relationship("DBItem", back_populates="armors")

    logger.debug("...effects")
    DBEffect.items = relationship("DBItem", secondary="item_effects", back_populates="effects")

    logger.debug("...mob")
    DBMob.npc = relationship("DBNpc", back_populates="mobs", uselist=False)
    DBMob.monster = relationship("DBMonster", back_populates="mobs", uselist=False)
    DBMob.directives = relationship("DBDirectives", secondary="mob_directives", back_populates="mobs")
    DBMob.player_race = relationship("DBPlayerRace", back_populates="mobs")
    DBMob.player_class = relationship("DBPlayerClass", back_populates="mobs")
    DBMob.mob_type = relationship("DBMOBType", back_populates="mobs")
    DBMob.room = relationship("DBRoom", back_populates="mobs")
    DBMob.attributes = relationship("DBAttribute", back_populates="mobs")
    DBMob.alignment = relationship("DBAlignment", back_populates="mobs")
    

    logger.debug("...npcs")
    DBNpc.mob = relationship("DBMob", back_populates="npcs")    
    DBNpc.directives = relationship("DBDirectivesNpcs", back_populates="npcs")

    logger.debug("...monsters")
    DBMonster.mob = relationship("DBMob", back_populates="monsters")
    DBMonster.directives = relationship("DBDirectivesMonsters", back_populates="monsters")

    logger.debug("...characters")
    DBCharacter.attributes = relationship("DBAttribute", back_populates="characters")
    DBCharacter.player_race = relationship("DBPlayerRace", back_populates="characters")
    DBCharacter.player_class = relationship("DBPlayerClass", back_populates="characters")
    DBCharacter.room = relationship("DBRoom", back_populates="characters")
    DBCharacter.alignment = relationship("DBAlignment", back_populates="characters")
    DBCharacter.role = relationship("DBRole", back_populates="characters")
    DBCharacter.player = relationship(back_populates="characters")

    logger.debug("...player races")
    DBPlayerRace.mobs = relationship("DBMob", back_populates="player_races")
    DBPlayerRace.directives = relationship("DBDirectivesRaces", back_populates="player_races")

    logger.debug("...player classes")
    DBPlayerClass.mobs = relationship("DBMob", back_populates="player_classes")
    DBPlayerRace.directives = relationship("DBDirectivesClasses", back_populates="player_classes")

    logger.debug("...players")
    DBPlayer.characters = relationship("DBCharacter", back_populates="players")

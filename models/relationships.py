from models.db_armor import DBArmor
from models.db_directions import DBDirection
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

def define_relationships():
    # Directions
    DBDirection.opposite = relationship("DBDirection", remote_side=[DBDirection.id], backref="reverse_direction")

    # Rooms
    DBRoom.exits = relationship("DBExit", back_populates="room")
    DBRoom.items = relationship("DBItem", back_populates="room")
    DBRoom.npcs = relationship("DBNpc", back_populates="room")
    DBRoom.monsters = relationship("DBMonster", back_populates="room")
    DBRoom.players = relationship("DBPlayer", back_populates="room")

    # Exits
    DBExit.room = relationship("DBRoom", back_populates="exits")

    # Items
    DBItem.room = relationship("DBRoom", back_populates="items")
    DBItem.food = relationship("DBFood", back_populates="item", uselist=False)
    DBItem.lightsource = relationship("DBLightsource", back_populates="item", uselist=False)
    DBItem.weapon = relationship("DBWeapon", back_populates="item", uselist=False)
    DBItem.armor = relationship("DBArmor", back_populates="item", uselist=False)
    DBItem.effects = relationship("DBEffect", secondary="item_effects", back_populates="items")

    # Food
    DBFood.item = relationship("DBItem", back_populates="food")
    DBFood.food_effects = relationship("DBFoodEffect", back_populates="food")

    # Lightsource
    DBLightsource.item = relationship("DBItem", back_populates="lightsource")

    # Weapon
    DBWeapon.item = relationship("DBItem", back_populates="weapon")

    # Armor
    DBArmor.item = relationship("DBItem", back_populates="armor")

    # Effects
    DBEffect.items = relationship("DBItem", secondary="item_effects", back_populates="effects")

    # Mobs
    DBMob.npc = relationship("DBNpc", back_populates="mob", uselist=False)
    DBMob.monster = relationship("DBMonster", back_populates="mob", uselist=False)
    DBMob.directives = relationship("DBDirectives", secondary="mob_directives", back_populates="directives")
    DBMob.player_race = relationship("DBPlayerRace", back_populates="mobs")
    DBMob.player_class = relationship("DBPlayerClass", back_populates="mobs")
    DBMob.mob_type = relationship("DBMOBType", back_populates="mobs")
    DBMob.room = relationship("DBRoom", back_populates="npcs")
    DBPlayer.attributes = relationship("DBAttribute", back_populates="attributes")

    # Npc
    DBNpc.mob = relationship("DBMob", back_populates="npc")    
    DBNpc.directives = relationship("DBDirectivesNpcs", back_populates="npc")

    # Monster
    DBMonster.mob = relationship("DBMob", back_populates="monster")
    DBMonster.directives = relationship("DBDirectivesMonsters", back_populates="monster")

    # Player
    DBPlayer.attributes = relationship("DBAttribute", back_populates="attributes")
    DBPlayer.race = relationship("DBPlayerRace", back_populates="players")
    DBPlayer.player_class = relationship("DBPlayerClass", back_populates="players")

    # PlayerRace
    DBPlayerRace.mobs = relationship("DBMob", back_populates="player_races")
    DBPlayerRace.directives = relationship("DBDirectivesRaces", back_populates="player_races")

    # PlayerClass
    DBPlayerClass.mobs = relationship("DBMob", back_populates="player_classes")
    DBPlayerRace.directives = relationship("DBDirectivesClasses", back_populates="player_classes")

    # # Directives
    # DBDirectives.npc_directives = relationship("DBNpc", back_populates="directives")
    # DBDirectives.monster_directives = relationship("DBMonster", back_populates="directives")
    # DBDirectives.race_directives = relationship("DBPlayerRace", back_populates="directives")
    # DBDirectives.class_directives = relationship("DBPlayerClass", back_populates="directives")

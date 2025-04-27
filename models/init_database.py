from sqlalchemy import inspect

# models
from models.base import Base
from models.association_tables import DBAssociations
from models.db_directives_classes import DBDirectivesClasses
from models.db_directives_monsters import DBDirectivesMonsters
from models.db_directives_npcs import DBDirectivesNpcs
from models.db_directives_races import DBDirectivesRaces
from models.db_mob_types import DBMOBType
from models.db_player_class import DBPlayerClass
from models.db_player_race import DBPlayerRace
from models.db_items import DBItem

from models.db_armor import DBArmor
from models.db_items_food import DBFood
from models.db_items_lightsources import DBLightsource
from models.db_items_weapons import DBWeapon
from models.db_mobs_npcs import DBNpc
from models.db_mobs_monsters import DBMonster
from models.db_mobs_players import DBPlayer
from models.db_mobs import DBMob
from models.db_room import DBRoom
from models.db_directions import DBDirection
from models.db_exit import DBExit
from models.db_environment import DBEnvironment
from models.db_directives import DBDirectives
from models.world_database import WorldDatabase
from models.db_effects import DBEffect
from source_data.directives_classes import DirectivesClassesSource
from source_data.directives_monsters import DirectivesMonsterSource
from source_data.directives_npcs import DirectivesNpcSource
from . import relationships 

from settings.global_settings import GlobalSettings
from source_data.armor import ArmorSource
from source_data.directions import DirectionsSource
from source_data.directives_race import DirectivesRacesSource
from source_data.directives_classes import DirectivesClassesSource
from source_data.directives_monsters import DirectivesMonsterSource
from source_data.directives_npcs import DirectivesNpcSource
from source_data.food import FoodSource
from source_data.effects import EffectSource
from source_data.lightsource import LightsourceSource
from source_data.mob_type import MobTypeSource
from source_data.monster import MonsterSource
from source_data.npc import NpcSource
from source_data.rooms import RoomSource
from source_data.weapon import WeaponSource
from utilities.log_telemetry import LogTelemetryUtility


class InitializeDatabase:
    logger = None
    db_path = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.db_path = GlobalSettings.DATABASE_STRING
        self.logger.debug("Initializing Database() class")
        self.logger.info(f"Database path: {self.db_path}")

    async def generate_rooms(self):
        pass

    async def populatedb(self):
        self.logger.debug("enter")
        world_db = WorldDatabase()

        try:
            # Create tables
            async with world_db.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            # Populate tables

            # mob type data
            mob_types_data = MobTypeSource().get_data()
            mt_dicts = [mt.to_dict() for mt in mob_types_data]
            await self.populate_table(DBMOBType, mt_dicts, world_db.async_session)

            # effects data
            effects_data = EffectSource().get_data()
            effects_dicts = [eff.to_dict() for eff in effects_data]
            await self.populate_table(DBEffect, effects_dicts, world_db.async_session)

            # room data
            room_data = RoomSource().get_data()
            room_dicts = [room.to_dict() for room in room_data]
            await self.populate_table(DBRoom, room_dicts, world_db.async_session)

            # armor data
            armor_data = ArmorSource().get_data()
            armor_dicts = [armor.to_dict() for armor in armor_data]
            await self.populate_item_and_related_tables(DBArmor, armor_dicts, world_db.async_session)

            # directives data - npc
            directives_data = DirectivesNpcSource().get_data()
            directives_dicts = [dir.to_dict() for dir in directives_data]
            await self.populate_table(DBDirectivesNpcs, directives_dicts, world_db.async_session)

            # directives data - monster
            directives_data = DirectivesMonsterSource().get_data()
            directives_dicts = [dir.to_dict() for dir in directives_data]
            await self.populate_table(DBDirectivesMonsters, directives_dicts, world_db.async_session)

            # directives data - race
            directives_data = DirectivesRacesSource().get_data()
            directives_dicts = [dir.to_dict() for dir in directives_data]
            await self.populate_table(DBDirectivesRaces, directives_dicts, world_db.async_session)

            # directives data - class
            directives_data = DirectivesClassesSource().get_data()
            directives_dicts = [dir.to_dict() for dir in directives_data]
            await self.populate_table(DBDirectivesClasses, directives_dicts, world_db.async_session)

            # food data
            food_data = FoodSource().get_data()
            food_dicts = [f.to_dict() for f in food_data]
            await self.populate_item_and_related_tables(DBFood, food_dicts, world_db.async_session)


            await self.populate_item_and_related_tables(
                DBLightsource, LightsourceSource().get_data(), world_db.async_session
            )
            await self.populate_item_and_related_tables(DBWeapon, WeaponSource().get_data(), world_db.async_session)
            await self.populate_table(DBDirection, DirectionsSource().get_data(), world_db.async_session)
            #await self.populate_table(DBMonster, MonsterSource().get_data(), world_db.async_session)
            #await self.populate_table(DBPlayerClass, PlayerClassSource().get_data(), world_db.async_session)
            #await self.populate_table(DBPlayerRace, PlayerRaceSource().get_data(), world_db.async_session)
            #await self.populate_table(DBNpc, NpcSource().get_data(), world_db.async_session)
            await self.populate_npc_and_related_tables(NpcSource(), world_db.async_session)
            await self.populate_monster_and_related_tables(MonsterSource(), world_db.async_session)
            #await self.populate_player_and_related_tables(PlayerSource(), world_db.async_session)

            # generate rooms - we now have everything we need
            # await self.generate_rooms()

            self.logger.debug("exit")

        except Exception as e:
            self.logger.error(f"Error populating database: {e}")

        finally:
            await world_db.close()

    async def populate_table(self, model_class, data, async_session):
        """Helper function to populate a table with data."""
        if not isinstance(data, list):
            data = [data]  # Ensure data is a list

        for item_data in data:
            try:
                async with async_session() as session:
                    async with session.begin():
                        db_item = model_class(**item_data)
                        session.add(db_item)
                        await session.flush()
            except Exception as e:
                self.logger.error(f"Error inserting data into \"{model_class.__tablename__.upper()}\":\nException: {e}")

    async def populate_npc_and_related_tables(self, npc_data_source, world_db_session):
        """Populates the mob and npc tables."""
        npc_data = npc_data_source.get_data()
        for npc_info in npc_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        mob_data = {
                            "name": npc_info.get("name"),
                            "pronoun": npc_info.get("pronoun"),
                            "description": npc_info.get("description"),
                            "hitpoints": npc_info.get("hitpoints"),
                            "damage_potential": npc_info.get("damage_potential"),
                            "experience": npc_info.get("experience"),
                            "money": npc_info.get("money"),
                            "room_name": npc_info.get("room_name"),
                        }
                        db_mob = DBMob(**mob_data)
                        session.add(db_mob)
                        await session.flush()  # Get the generated mob.id

                        npc_specific_data = {
                            "mob_id": db_mob.id,
                            "title": npc_info.get("title"),
                            "interests": npc_info.get("interests"),
                            "npc_type": npc_info.get("npc_type"),
                            "wanders": npc_info.get("wanders"),
                        }
                        db_npc = DBNpc(**npc_specific_data)
                        session.add(db_npc)
                        self.logger.debug(f"Inserted NPC '{npc_info.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting NPC '{npc_info.get('name')}': {e}")

    async def populate_monster_and_related_tables(self, monster_data_source, world_db_session):
        """Populates the mob and monster tables."""
        monster_data = monster_data_source.get_data()
        for monster_info in monster_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        mob_data = {
                            "name": monster_info.get("name"),
                            "pronoun": monster_info.get("pronoun"),
                            "description": monster_info.get("description"),
                            "hitpoints": monster_info.get("hitpoints"),
                            "damage_potential": monster_info.get("damage_potential"),
                            "experience": monster_info.get("experience"),
                            "money": monster_info.get("money"),
                            "room_name": monster_info.get("room_name"),
                        }
                        db_mob = DBMob(**mob_data)
                        session.add(db_mob)
                        await session.flush()  # Get the generated mob.id

                        monster_specific_data = {
                            "mob_id": db_mob.id,
                            "type": monster_info.get("type"),
                            "alignment": monster_info.get("alignment"),
                            "possible_adjectives": monster_info.get("possible_adjectives"),
                            "adjective_chance": monster_info.get("adjective_chance"),
                            "respawn_rate_secs": monster_info.get("respawn_rate_secs"),
                            "dead_epoch": monster_info.get("dead_epoch"),
                            "wanders": monster_info.get("wanders"),
                            "death_cry": monster_info.get("death_cry"),
                            "entrance_cry": monster_info.get("entrance_cry"),
                            "victory_cry": monster_info.get("victory_cry"),
                            "flee_cry": monster_info.get("flee_cry"),
                        }
                        db_monster = DBMonster(**monster_specific_data)
                        session.add(db_monster)
                        self.logger.debug(f"Inserted Monster '{monster_info.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Monster '{monster_info.get('name')}': {e}")

    async def populate_player_and_related_tables(self, player_data_source, world_db_session):
        """Populates the mob and player tables."""
        player_data = player_data_source.get_data()
        for player_info in player_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        mob_data = {
                            "name": player_info.get("name"),
                            "pronoun": player_info.get("pronoun"),
                            "description": player_info.get("description"),
                            "hitpoints": player_info.get("hitpoints"),
                            "damage_potential": player_info.get("damage_potential"),
                            "experience": player_info.get("experience"),
                            "money": player_info.get("money"),
                            "room_name": player_info.get("room_name"),
                        }
                        db_mob = DBMob(**mob_data)
                        session.add(db_mob)
                        await session.flush()  # Get the generated mob.id

                        player_specific_data = {
                            "mob_id": db_mob.id,
                            # Add any player-specific fields here if you have them in your source data
                        }
                        db_player = DBPlayer(**player_specific_data)
                        session.add(db_player)
                        self.logger.debug(f"Inserted Player '{player_info.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Player '{player_info.get('name')}': {e}")


    async def populate_item_and_related_tables(self, model_class, data, async_session):
        """Helper function to populate item-related tables."""
        if not isinstance(data, list):
            data = [data]

        for item_data in data:
            try:
                async with async_session() as session:
                    async with session.begin():
                        # Create DBItem
                        db_item = DBItem(
                            name=item_data["name"],
                            item_type=item_data["item_type"],
                            weight=item_data["weight"],
                            verb=item_data["verb"],
                            plural_verb=item_data["plural_verb"],
                            description=item_data["description"],
                            room_name=item_data.get("room_name"),
                        )
                        session.add(db_item)
                        await session.flush()

                        mapper = inspect(model_class)  # dynamically gets the fields of the model class
                        model_fields = set(c.key for c in mapper.attrs)
                        filtered_data = {k: v for k, v in item_data.items() if k in model_fields}
                        self.logger.debug(f"Inserting {model_class.__name__} with fields: {filtered_data}")
                        db_specific_item = model_class(id=db_item.id, **filtered_data)
                        db_specific_item.item_id = db_item.id
                        session.add(db_specific_item)

                        await session.flush()
            except Exception as e:
                self.logger.error(f"Error inserting data into {model_class.__tablename__}: {e}")

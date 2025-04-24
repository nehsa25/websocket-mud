import asyncio
import os

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# models
from models.base import Base
from models.db_directives import DBDirectives
from models.db_effects import DBEffect
from models.db_exit import DBExit
from models.db_item import DBItem
from models.db_armor import DBArmor
from models.db_player import DBPlayer
from models.db_room import DBRoom
from models.db_directions import DBDirection
from models.db_food import DBFood
from models.db_lightsource import DBLightsource
from models.db_player_class import DBPlayerClass
from models.db_player_race import DBPlayerRace
from models.db_weapon import DBWeapon
from models.db_npc import DBNpc
from models.db_monster import DBMonster

from settings.global_settings import GlobalSettings
from source_data.armor import ArmorSource
from source_data.directions import DirectionsSource
from source_data.directives import DirectivesSource
from source_data.food import FoodSource
from source_data.effects import EffectSource
from source_data.lightsource import LightsourceSource
from source_data.monster import MonsterSource
from source_data.npc import NpcSource
from source_data.player_class import PlayerClassSource
from source_data.player_race import PlayerRaceSource
from source_data.rooms import RoomSource
from source_data.weapon import WeaponSource
from class_types.room_type import RoomType
from utilities.log_telemetry import LogTelemetryUtility
from models.world_database import WorldDatabase


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


            # effects data
            effects_data = EffectSource().get_data()
            effects_dicts = [eff.to_dict() for eff in effects_data]
            await self.populate_table(DBEffect, effects_dicts, world_db.async_session)
            room_data = RoomSource().get_data()
            room_dicts = [room.to_dict() for room in room_data]
            await self.populate_table(DBRoom, room_dicts, world_db.async_session)
            await self.populate_item_related_table(DBArmor, ArmorSource().get_data(), world_db.async_session)
            await self.populate_item_related_table(DBFood, FoodSource().get_data(), world_db.async_session)
            await self.populate_item_related_table(DBLightsource, LightsourceSource().get_data(), world_db.async_session)
            await self.populate_item_related_table(DBWeapon, WeaponSource().get_data(), world_db.async_session)
            await self.populate_table(DBDirectives, DirectivesSource().get_data(), world_db.async_session)
            await self.populate_table(DBDirection, DirectionsSource().get_data(), world_db.async_session)
            await self.populate_table(DBMonster, MonsterSource().get_data(), world_db.async_session)
            await self.populate_table(DBPlayerClass, PlayerClassSource().get_data(), world_db.async_session)
            await self.populate_table(DBPlayerRace, PlayerRaceSource().get_data(), world_db.async_session)
            await self.populate_table(DBNpc, NpcSource().get_data(), world_db.async_session)

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
                self.logger.error(f"Error inserting data into {model_class.__tablename__}: {e}")

    async def populate_item_related_table(self, model_class, data, async_session):
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
                            room_name = item_data["room_name"]
                        )
                        session.add(db_item)
                        await session.flush()

                        # Create specific item type (e.g., DBArmor)
                        db_specific_item = model_class(**item_data)
                        db_specific_item.item_id = db_item.id  # Link to DBItem
                        session.add(db_specific_item)

                        await session.flush()
            except Exception as e:
                self.logger.error(f"Error inserting data into {model_class.__tablename__}: {e}")

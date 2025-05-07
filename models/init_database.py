import json
from sqlalchemy import inspect, select
from core.enums.mob_types import MobTypeEnum
from models.db_alignments import DBAlignments
from models.db_environment import DBEnvironment
from models.db_exits import DBExit
from models.db_player_race import DBPlayerRace
from settings.global_settings import GlobalSettings
from source_data.alignments import AlignmentsSource
from source_data.environments import EnvironmentsSource
from source_data.mobs_npcs import NpcSource
from source_data.player_race import PlayerRaceSource
from utilities.log_telemetry import LogTelemetryUtility


# models
from models.base import Base
from models.db_attributes import DBAttributes
from models.db_mob_types import DBMOBType
from models.db_player_class import DBPlayerClass
from models.db_items import DBItem
from models.db_armor import DBArmor
from models.db_items_food import DBFood
from models.db_items_lightsources import DBLightsource
from models.db_items_weapons import DBWeapon
from models.db_mobs_npcs import DBNpc
from models.db_mobs_monsters import DBMonster
from models.db_players import DBPlayer
from models.db_mobs import DBMob
from models.db_role import DBRole
from models.db_room import DBRoom
from models.db_directions import DBDirection
from models.world_database import WorldDatabase
from models.db_effects import DBEffect

# sources

from source_data.player import PlayerSource
from source_data.player_class import PlayerClassSource
from source_data.roles import RoleSource
from source_data.armor import ArmorSource
from source_data.directions import DirectionsSource
from source_data.food import FoodSource
from source_data.effects import EffectSource
from source_data.lightsource import LightsourceSource
from source_data.mob_type import MobTypeSource
from source_data.mobs_monsters import MonsterSource
from source_data.rooms import RoomSource
from source_data.weapon import WeaponSource


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

            # alignments data
            alignments_data = AlignmentsSource().get_data()
            ad_dicts = [ad.to_dict() for ad in alignments_data]
            await self.populate_table(DBAlignments, ad_dicts, world_db.async_session)

            # environments
            environments_data = EnvironmentsSource().get_data()
            ed_dicts = [ed.to_dict() for ed in environments_data]
            await self.populate_table(DBEnvironment, ed_dicts, world_db.async_session)

            # room data
            room_data = RoomSource().get_data()
            room_dicts = [room.to_dict() for room in room_data]
            await self.populate_room_and_related_tables(room_dicts, world_db.async_session)

            # mob type data
            mob_types_data = MobTypeSource().get_data()
            mt_dicts = [mt.to_dict() for mt in mob_types_data]
            await self.populate_table(DBMOBType, mt_dicts, world_db.async_session)

            # effects data
            effects_data = EffectSource().get_data()
            effects_dicts = [eff.to_dict() for eff in effects_data]
            await self.populate_table(DBEffect, effects_dicts, world_db.async_session)

            # role data
            role_data = RoleSource().get_data()
            role_dicts = [r.to_dict() for r in role_data]
            await self.populate_table(DBRole, role_dicts, world_db.async_session)

            # player class data
            playerclass_data = PlayerClassSource().get_data()
            pcd_dicts = [pcd.to_dict() for pcd in playerclass_data]
            await self.populate_player_classes(pcd_dicts, world_db.async_session)

            # player race data
            playerrace_data = PlayerRaceSource().get_data()
            prd_dicts = [prd.to_dict() for prd in playerrace_data]
            await self.populate_race_and_related_tables(prd_dicts, world_db.async_session)

            # player data
            player_data = PlayerSource().get_data()
            player_dicts = [p.to_dict() for p in player_data]
            await self.populate_player_and_related_tables(player_dicts, world_db.async_session)

            # monster data
            monster_data = MonsterSource().get_data()
            monsters_dicts = [m.to_dict() for m in monster_data]
            await self.populate_monster_and_related_tables(monsters_dicts, world_db.async_session)

            # npc data
            npc_data = NpcSource().get_data()
            npc_dicts = [nd.to_dict() for nd in npc_data]
            await self.populate_npc_and_related_tables(npc_dicts, world_db.async_session)

            # food data
            food_data = FoodSource().get_data()
            food_dicts = [f.to_dict() for f in food_data]
            await self.populate_item_and_related_tables(DBFood, food_dicts, world_db.async_session)

            # lightsource data
            lightsource_data = LightsourceSource().get_data()
            ls_dicts = [ls.to_dict() for ls in lightsource_data]
            await self.populate_item_and_related_tables(DBLightsource, ls_dicts, world_db.async_session)

            # armor data
            armor_data = ArmorSource().get_data()
            armor_dicts = [armor.to_dict() for armor in armor_data]
            await self.populate_item_and_related_tables(DBArmor, armor_dicts, world_db.async_session)

            # weapon data
            weapon_data = WeaponSource().get_data()
            wd_dicts = [wd.to_dict() for wd in weapon_data]
            await self.populate_item_and_related_tables(DBWeapon, wd_dicts, world_db.async_session)

            # directions data
            directions_data = DirectionsSource().get_data()
            directions_dicts = [dir.to_dict() for dir in directions_data]
            await self.populate_table(DBDirection, directions_dicts, world_db.async_session)

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
                self.logger.error(f'Error inserting data into "{model_class.__tablename__.upper()}":\nException: {e}')

    async def populate_player_classes(self, player_data_source, world_db_session):
        """Populates the player and attributes tables."""
        player_data = player_data_source
        for p_data in player_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBAttributes
                        attributes_data = p_data.get("attributes", {})
                        db_attributes = DBAttributes(**attributes_data)
                        session.add(db_attributes)
                        await session.flush()

                        db_player_class = DBPlayerClass(
                            name=p_data.get("name"),
                            description=p_data.get("description"),
                            abilities=json.dumps(p_data.get("abilities")),
                            directives=json.dumps(p_data.get("directives")) if p_data.get("directives") else None,
                            base_experience_adjustment=p_data.get("base_experience_adjustment"),
                            playable=p_data.get("playable"),
                            attributes_id=db_attributes.id,
                        )
                        session.add(db_player_class)
                        await session.commit()
                        self.logger.debug(f"Inserted Class: '{p_data.get('name')}'")
            except Exception as e:
                self.logger.error(f"Error inserting class '{p_data.get('name')}': {e}")
    
    async def populate_room_and_related_tables(self, room_data_source, world_db_session):
        """Populates the room and attributes tables."""
        for p_data in room_data_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBExit the exit information
                        exits_data = p_data.get("exits", {})

                        # Convert ExitData to a dictionary if it's not already
                        if not isinstance(exits_data, dict):
                            exits_data = exits_data.to_dict()

                        db_exit = DBExit(**exits_data)
                        session.add(db_exit)
                        await session.flush()

                        # get environment from environment_id
                        environment = await session.get(DBEnvironment, p_data.get("environment_id"))

                        # Insert into DBRoom
                        db_room = DBRoom(
                            name=p_data.get("name"),
                            environment_id=environment.id if environment else None,
                            description=p_data.get("description"),
                            inside=p_data.get("inside"),
                            room_id=p_data.get("room_id"),
                            exits_id=db_exit.id,
                        )
                        session.add(db_room)
                        await session.flush()

                        self.logger.debug(f"Inserted race: '{p_data.get('name')}'")
            except Exception as e:
                self.logger.error(f"Error inserting race '{p_data.get('name')}': {e}")

    async def populate_race_and_related_tables(self, player_data_source, world_db_session):
        """Populates the player and attributes tables."""
        player_data = player_data_source
        for p_data in player_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBAttributes
                        attributes_data = p_data.get("attributes", {})
                        db_attributes = DBAttributes(**attributes_data)
                        session.add(db_attributes)
                        await session.flush()

                        # Insert into DBPlayerRace
                        directives = p_data.get("directives")
                        db_player_race = DBPlayerRace(
                            name=p_data.get("name"),
                            description=p_data.get("description"),
                            abilities=json.dumps(p_data.get("abilities")),
                            directives=json.dumps(directives) if directives else None,
                            playable=p_data.get("playable"),
                            base_experience_adjustment=p_data.get("base_experience_adjustment"),
                            attributes_id=db_attributes.id,
                        )
                        session.add(db_player_race)
                        await session.flush()

                        self.logger.debug(f"Inserted race: '{p_data.get('name')}'")
            except Exception as e:
                self.logger.error(f"Error inserting race '{p_data.get('name')}': {e}")

    async def populate_player_and_related_tables(self, player_data_source, world_db_session):
        """Populates the player and attributes tables."""
        player_data = player_data_source
        for p_data in player_data:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBAttributes
                        attributes_data = p_data.get("attributes", {})
                        db_attributes = DBAttributes(**attributes_data)
                        session.add(db_attributes)
                        await session.flush()

                        # get room from room_id
                        room = await session.get(DBRoom, p_data.get("room_id"))

                        # Find PlayerRace
                        race_name = p_data.get("player_race")
                        race_result = await session.execute(
                            select(DBPlayerRace).where(DBPlayerRace.name == race_name)
                        )
                        db_race = race_result.scalar_one_or_none()

                        # Find PlayerClass
                        class_name = p_data.get("player_class")
                        class_result = await session.execute(
                            select(DBPlayerClass).where(DBPlayerClass.name == class_name)
                        )
                        db_class = class_result.scalar_one_or_none()

                        # Find Role
                        role_name = p_data.get("role")
                        role_result = await session.execute(
                            select(DBRole).where(DBRole.name == role_name)
                        )
                        db_role = role_result.scalar_one_or_none()

                        # Insert into DBPlayer
                        db_player = DBPlayer(
                            name=p_data.get("name"),
                            role_id=db_role.id if db_role else None,
                            level=p_data.get("level"),
                            pronoun=p_data.get("pronoun"),
                            experience=p_data.get("experience"),
                            money=p_data.get("money"),
                            token=p_data.get("token"),
                            pin=p_data.get("pin"),
                            salt=p_data.get("salt"),
                            attributes_id=db_attributes.id,
                            room_id=room.id if room else None,
                            race_id=db_race.id if db_race else None,
                            class_id=db_class.id if db_class else None,
                        )
                        session.add(db_player)
                        await session.commit()
                        self.logger.debug(f"Inserted Player: '{p_data.get('name')}' with id: {db_player.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Player '{p_data.get('name')}': {e}")

    async def populate_npc_and_related_tables(self, npc_data_source, world_db_session):
        """Populates the mob and npc tables."""
        for npc_info in npc_data_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBAttributes
                        attributes_data = npc_info.get("attributes", {})
                        db_attributes = DBAttributes(**attributes_data)
                        session.add(db_attributes)
                        await session.flush()

                        # Find PlayerRace
                        race_name = npc_info.get("race_name")
                        race_result = await session.execute(
                            select(DBPlayerRace).where(DBPlayerRace.name == race_name)
                        )
                        db_race = race_result.scalar_one_or_none()

                        # Find PlayerClass
                        class_name = npc_info.get("class_name")
                        class_result = await session.execute(
                            select(DBPlayerClass).where(DBPlayerClass.name == class_name)
                        )
                        db_class = class_result.scalar_one_or_none()

                        # Find Alignment
                        alignment_name = npc_info.get("alignment")
                        alignment_result = await session.execute(
                            select(DBAlignments).where(DBAlignments.name == alignment_name)
                        )
                        db_alignment = alignment_result.scalar_one_or_none()

                        # Find mobtype
                        mobtype_name = MobTypeEnum.NPC.value
                        mobtype_result = await session.execute(
                            select(DBMOBType).where(DBMOBType.type == mobtype_name)
                        )
                        db_mobtype = mobtype_result.scalar_one_or_none()                                  

                        mob_data = {
                            "name": npc_info.get("name"),
                            "pronoun": npc_info.get("pronoun"),
                            "description": npc_info.get("description"),
                            "damage_potential": npc_info.get("damage_potential"),
                            "experience": npc_info.get("experience"),
                            "money": npc_info.get("money"),
                            "room_id": npc_info.get("room_id"),
                            "alignment_id": db_alignment.id,
                            "attributes_id": db_attributes.id,
                            "mob_type_id": db_mobtype.id,
                            "death_cry": npc_info.get("death_cry"),
                            "entrance_cry": npc_info.get("entrance_cry"),
                            "victory_cry": npc_info.get("victory_cry"),
                            "flee_cry": npc_info.get("flee_cry"),
                            "attributes": npc_info.get("attributes"),
                            "race_id": db_race.id,
                            "class_id": db_class.id,
                            "respawn_rate_secs": npc_info.get("respawn_rate_secs"),
                            "wanders": npc_info.get("wanders"),
                        }
                        db_mob = DBMob(**mob_data)
                        session.add(db_mob)
                        await session.flush()  # Get the generated mob.id

                        npc_specific_data = {
                            "mob_id": db_mob.id,
                            "title": npc_info.get("title"),
                            "interests": npc_info.get("interests"),
                        }
                        db_npc = DBNpc(**npc_specific_data)
                        session.add(db_npc)
                        self.logger.debug(f"Inserted NPC '{npc_info.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting NPC '{npc_info.get('name')}': {e}")

    async def populate_monster_and_related_tables(self, monster_data_source, world_db_session):
        """Populates the mob and monster tables."""
        for monster_info in monster_data_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Insert into DBAttributes
                        attributes_data = monster_info.get("attributes", {})
                        db_attributes = DBAttributes(**attributes_data)
                        session.add(db_attributes)
                        await session.flush()

                        # Find PlayerRace
                        race_name = monster_info.get("race_name")
                        race_result = await session.execute(
                            select(DBPlayerRace).where(DBPlayerRace.name == race_name)
                        )
                        db_race = race_result.scalar_one_or_none()

                        # Find PlayerClass
                        class_name = monster_info.get("class_name")
                        class_result = await session.execute(
                            select(DBPlayerClass).where(DBPlayerClass.name == class_name)
                        )
                        db_class = class_result.scalar_one_or_none()

                        # Find Alignment
                        alignment_name = monster_info.get("alignment")
                        alignment_result = await session.execute(
                            select(DBAlignments).where(DBAlignments.name == alignment_name)
                        )
                        db_alignment = alignment_result.scalar_one_or_none()

                        # Find mobtype
                        mobtype_name = MobTypeEnum.MONSTER.value
                        mobtype_result = await session.execute(
                            select(DBMOBType).where(DBMOBType.type == mobtype_name)
                        )
                        db_mobtype = mobtype_result.scalar_one_or_none()                        

                        mob_data = {
                            "name": monster_info.get("name"),
                            "pronoun": monster_info.get("pronoun"),
                            "description": monster_info.get("description"),
                            "damage_potential": monster_info.get("damage_potential"),
                            "experience": monster_info.get("experience"),
                            "money": monster_info.get("money"),
                            "room_id": monster_info.get("room_id"),
                            "attributes_id": db_attributes.id,
                            "alignment_id": db_alignment.id,
                            "mob_type_id": db_mobtype.id,
                            "death_cry": monster_info.get("death_cry"),
                            "entrance_cry": monster_info.get("entrance_cry"),
                            "victory_cry": monster_info.get("victory_cry"),
                            "flee_cry": monster_info.get("flee_cry"),
                            "attributes": monster_info.get("attributes"),
                            "race_id": db_race.id,
                            "class_id": db_class.id,
                            "respawn_rate_secs": monster_info.get("respawn_rate_secs"),
                            "wanders": monster_info.get("wanders"),
                        }
                        db_mob = DBMob(**mob_data)
                        session.add(db_mob)
                        await session.flush()  # Get the generated mob.id

                        monster_specific_data = {
                            "mob_id": db_mob.id,
                            "possible_adjectives": monster_info.get("possible_adjectives"),
                            "adjective_chance": monster_info.get("adjective_chance"),
                        }
                        db_monster = DBMonster(**monster_specific_data)
                        session.add(db_monster)
                        self.logger.debug(f"Inserted Monster '{monster_info.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Monster '{monster_info.get('name')}': {e}")

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

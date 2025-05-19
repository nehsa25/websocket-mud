import json
from sqlalchemy import inspect, select
from core.enums.alignments import AlignmentEnum
from core.enums.mob_types import MobTypeEnum
from models.db_alignments import DBAlignment
from models.db_characters import DBCharacter
from models.db_environment import DBEnvironment
from models.db_exits import DBExit
from models.db_player_race import DBPlayerRace
from models.relationships import define_relationships
from settings.global_settings import GlobalSettings
from source_data.alignments import AlignmentsSource
from source_data.character import CharacterSource
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
        # define_relationships()

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
            await self.populate_table(DBAlignment, ad_dicts, world_db.async_session)

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

    async def populate_mob_item(self, mob_type, info, the_sess):
        # Insert into DBAttributes
        db_attributes = info.get("attributes", {})
        db_attributes = DBAttributes(**db_attributes)
        the_sess.add(db_attributes)
        await the_sess.flush()

        # Find PlayerRace
        player_race = info.get("player_race")
        player_race_result = await the_sess.execute(select(DBPlayerRace).where(DBPlayerRace.name == player_race))
        db_player_race: DBPlayerRace = player_race_result.scalar_one_or_none()
        if db_player_race is None:
            raise Exception("PlayerRace not found: {}", player_race)

        # Find PlayerClass
        player_class = info.get("player_class")
        player_class_result = await the_sess.execute(select(DBPlayerClass).where(DBPlayerClass.name == player_class))
        db_player_class: DBPlayerClass = player_class_result.scalar_one_or_none()
        if db_player_class is None:
            raise Exception("PlayerClass not found: {}", player_class)

        # Find Alignment
        alignment_name = info.get("alignment")
        alignment_result = await the_sess.execute(select(DBAlignment).where(DBAlignment.name == alignment_name))
        db_alignment: DBAlignment = alignment_result.scalar_one_or_none()

        # Find mobtype
        mobtype_name = mob_type
        mobtype_result = await the_sess.execute(select(DBMOBType).where(DBMOBType.type == mobtype_name))
        db_mobtype: DBMOBType = mobtype_result.scalar_one_or_none()

        db_mob = DBMob(
            name=info.get("name"),
            pronoun=info.get("pronoun"),
            level=info.get("level"),
            description=info.get("description"),
            experience=info.get("experience"),
            money=info.get("money"),
            title=info.get("title"),
            room_id=info.get("room_id"),
            alignment_id=db_alignment.id,
            attributes_id=db_attributes.id,
            mob_type_id=db_mobtype.id,
            attributes=info.get("attributes"),
            player_race_id=db_player_race.id,
            player_class_id=db_player_class.id
        )
        the_sess.add(db_mob)
        await the_sess.flush()  # Get the generated mob.id

        return db_mob

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
                        environment_result = await session.execute(
                            select(DBEnvironment).where(DBEnvironment.name == p_data.get("environment_name"))
                        )
                        environment = environment_result.scalar_one_or_none()
                        if not environment:
                            raise Exception("Environment not found: {}".format(p_data.get("environment_name")))

                        # Insert into DBRoom
                        db_room = DBRoom(
                            room_id=p_data.get("room_id"),
                            name=p_data.get("name"),
                            description=p_data.get("description"),
                            environment_id=environment.id if environment else None,
                            monsters=p_data.get("monsters"),
                            items=p_data.get("items"),
                            npcs=p_data.get("npcs"),
                            characters=p_data.get("characters"),
                            exit_id=db_exit.id if db_exit else None,
                            inside=p_data.get("inside"),
                        )
                        session.add(db_room)
                        await session.flush()

                        self.logger.debug(f"Inserted room: '{p_data.get('name')}'")
            except Exception as e:
                self.logger.error(f"Error inserting room '{p_data.get('name')}': {e}")

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
        player_source = player_data_source
        for p_data in player_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        # Find Role
                        role_name = p_data.get("role")
                        role_result = await session.execute(select(DBRole).where(DBRole.name == role_name))
                        db_role: DBRole = role_result.scalar_one_or_none()
                        if not db_role:
                            raise Exception("Role not found: {}".format(role_name))

                        # Insert into DBPlayer
                        db_player = DBPlayer(
                            firstname=p_data.get("firstname"),
                            lastname=p_data.get("lastname"),
                            role_id=db_role.id if db_role else None,
                            email=p_data.get("email"),
                            pin=p_data.get("pin"),
                            salt=p_data.get("salt"),
                        )
                        session.add(db_player)
                        await session.flush()

                        # character data
                        character_source = CharacterSource().get_data()
                        characters_dicts = [cd.to_dict() for cd in character_source]
                        for c_data in characters_dicts:
                            db_mob: DBMob = await self.populate_mob_item(MobTypeEnum.PLAYER.value, c_data, session)

                            db_character = DBCharacter(
                                firstname=c_data.get("firstname"),
                                lastname=c_data.get("lastname"),
                                eye_brow=c_data.get("eye_brow"),
                                eye_color=c_data.get("eye_color"),
                                body_type=c_data.get("body_type"),
                                facial_hair=c_data.get("facial_hair"),
                                hair_color=c_data.get("hair_color"),
                                hair_style=c_data.get("hair_style"),
                                role_id=db_role.id,
                                player_id=db_player.id,
                                mob_id=db_mob.id,
                            )
                            session.add(db_character)
                            await session.flush()

                        # Commit the changes to the database
                        await session.commit()
                        self.logger.debug(f"Inserted Player: '{p_data.get('name')}' with id: {db_player.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Player '{p_data.get('name')}': {e}")
                pass

    async def populate_npc_and_related_tables(self, npc_data_source, world_db_session):
        """Populates the mob and npc tables."""
        for npc_source in npc_data_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        db_mob = await self.populate_mob_item(MobTypeEnum.NPC.value, npc_source, session)

                        db_npc = DBNpc(
                            mob_id=db_mob.id,
                            interests=npc_source.get("interests"),
                            respawn_rate_secs=npc_source.get("respawn_rate_secs"),
                            wanders=npc_source.get("wanders"),
                            death_cry=npc_source.get("death_cry"),
                            entrance_cry=npc_source.get("entrance_cry"),
                            victory_cry=npc_source.get("victory_cry"),
                            flee_cry=npc_source.get("flee_cry"),
                        )
                        session.add(db_npc)
                        self.logger.debug(f"Inserted NPC '{npc_source.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting NPC '{npc_source.get('name')}': {e}")
                pass

    async def populate_monster_and_related_tables(self, monster_data_source, world_db_session):
        """Populates the mob and monster tables."""
        for monster_source in monster_data_source:
            try:
                async with world_db_session() as session:
                    async with session.begin():
                        db_mob = await self.populate_mob_item(MobTypeEnum.MONSTER.value, monster_source, session)

                        db_monster = DBMonster(
                            mob_id=db_mob.id,
                            possible_adjectives=monster_source.get("possible_adjectives"),
                            adjective_chance=monster_source.get("adjective_chance"),
                            respawn_rate_secs=monster_source.get("respawn_rate_secs"),
                            wanders=monster_source.get("wanders"),
                            death_cry=monster_source.get("death_cry"),
                            entrance_cry=monster_source.get("entrance_cry"),
                            victory_cry=monster_source.get("victory_cry"),
                            flee_cry=monster_source.get("flee_cry"),
                        )
                        session.add(db_monster)
                        self.logger.debug(f"Inserted Monster '{monster_source.get('name')}' with mob_id: {db_mob.id}")

            except Exception as e:
                self.logger.error(f"Error inserting Monster '{monster_source.get('name')}': {e}")
                pass

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

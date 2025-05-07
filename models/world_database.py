from sqlalchemy import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.enums.alignments import AlignmentEnum
from models.db_attributes import DBAttributes
from models.db_players import DBPlayer
from settings.global_settings import GlobalSettings
from utilities.log_telemetry import LogTelemetryUtility

Base = declarative_base()


class WorldDatabase:
    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing WorldDatabase")
        self.db_url = GlobalSettings.DATABASE_STRING
        self.engine = create_async_engine(self.db_url, echo=True)  # Use async engine
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def close(self):
        await self.engine.dispose()

    async def update_player(self, player):
        """Updates the player's information in the database, inserting if it doesn't exist."""
        self.logger.debug("enter")
        player_id = None
        try:
            async with self.async_session() as session:
                async with session.begin():
                    # Find the player in the database
                    player_result = await session.execute(
                        select(DBPlayer).where(DBPlayer.name == player.name)
                    )
                    db_player = player_result.scalar_one_or_none()

                    # TODO: not setup yet
                    if db_player:
                        # Update the player's attributes
                        db_player.level = player.level
                        db_player.experience = player.experience
                        db_player.room_id = player.room_id
                        db_player.race_id = player.race_id
                        db_player.class_id = player.class_id
                        db_player.alignment_id = player.alignment_id
                        db_player.attributes_id = player.attributes_id

                        self.logger.info(f"Player '{player.name}' updated in the database.")
                    else:
                        # initial attributes
                        db_attributes = DBAttributes(
                            strength=10,
                            dexterity=10,
                            constitution=10,
                            intelligence=10,
                            wisdom=10,
                            charisma=10,
                        )
                        session.add(db_attributes)
                        await session.flush()

                        # Create a new player object
                        db_player = DBPlayer(
                            name=player.name,
                            level=player.level,
                            experience=player.experience,
                            room_id=1,
                            race_id=1,
                            class_id=1,
                            money=0,
                            token=player.token,
                            pronoun="he",
                            alignment_id=AlignmentEnum.NEUTRAL.value,
                            attributes_id=db_attributes.id
                        )
                        session.add(db_player)
                        await session.flush()
                        player_id = db_player.id
                        self.logger.info(f"Player '{player.name}' created in the database ID: {db_player.id}.")

                    # Commit the changes to the database
                    await session.commit()

                    return player_id

        except Exception as e:
            self.logger.error(f"Error updating player '{player.name}' in the database: {e}")
        self.logger.debug("exit")
        return player_id

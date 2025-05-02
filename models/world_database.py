from sqlalchemy import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.db_players import DBPlayer
from settings.global_settings import GlobalSettings

Base = declarative_base()


class WorldDatabase:
    def __init__(self):
        self.db_url = GlobalSettings.DATABASE_STRING
        self.engine = create_async_engine(self.db_url, echo=True)  # Use async engine
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def close(self):
        await self.engine.dispose()

    async def update_player(self, player):
        """Updates the player's information in the database, inserting if it doesn't exist."""
        self.logger.debug("enter")
        try:
            async with self.world_db_session() as session:
                async with session.begin():
                    # Find the player in the database
                    player_result = await session.execute(
                        select(DBPlayer).where(DBPlayer.name == player.name)
                    )
                    db_player = player_result.scalar_one_or_none()

                    if db_player:
                        # Update the player's attributes
                        db_player.description = player.description
                        db_player.level = player.level
                        db_player.experience = player.experience
                        db_player.money = player.money
                        db_player.room_id = player.room_id
                        db_player.race_id = player.race_id
                        db_player.class_id = player.class_id
                        db_player.alignment_id = player.alignment_id
                        db_player.attributes_id = player.attributes_id

                        self.logger.info(f"Player '{player.name}' updated in the database.")
                    else:
                        # Create a new player object
                        db_player = DBPlayer(
                            name=player.name,
                            description=player.description,
                            level=player.level,
                            experience=player.experience,
                            money=player.money,
                            room_id=player.room_id,
                            race_id=player.race_id,
                            class_id=player.class_id,
                            alignment_id=player.alignment_id,
                            attributes_id=player.attributes_id,
                        )
                        session.add(db_player)
                        self.logger.info(f"Player '{player.name}' created in the database.")

                    # Commit the changes to the database
                    await session.commit()
                    

        except Exception as e:
            self.logger.error(f"Error updating player '{player.name}' in the database: {e}")
        self.logger.debug("exit")

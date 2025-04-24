from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings.global_settings import GlobalSettings

Base = declarative_base()


class WorldDatabase:
    def __init__(self):
        self.db_url = GlobalSettings.DATABASE_STRING
        self.engine = create_async_engine(self.db_url, echo=True)  # Use async engine
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def close(self):
        await self.engine.dispose()

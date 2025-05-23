from models.db_armor_types import DBArmorTypes
from models.world_database import WorldDatabase
from sqlalchemy.future import select

_armor_type_lookup = None

async def load_armor_type_lookup(world_db: WorldDatabase):
    global _armor_type_lookup
    if _armor_type_lookup is None:
        async with world_db.async_session() as session:
            result = await session.execute(select(DBArmorTypes))
            armor_types = result.scalars().all()
            _armor_type_lookup = {at.name: at for at in armor_types}
    return _armor_type_lookup

async def get_armor_type_by_name(name: str, world_db: WorldDatabase):
    if _armor_type_lookup is None:
        await load_armor_type_lookup(world_db)
    return _armor_type_lookup.get(name)
# fixtures
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


from dontcheckin import Secrets

DATABASE_URL = Secrets.DATABASE


@pytest.fixture(scope="session")
def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    # pytest-asyncio does not support async yield in session scope cleanly


@pytest.fixture
async def async_session(db_engine):
    async_sessionmaker = sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_sessionmaker() as session:
        yield session

async def get_table_record_count_sqlalchemy(engine: AsyncEngine, table_name: str) -> int:
    try:
        async_sessionmaker = sessionmaker(bind=engine, class_=AsyncSession)
        async with async_sessionmaker() as session:
            result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar_one_or_none()
            return count if count is not None else 0
    except Exception as e:
        pytest.fail(f"SQLAlchemy error: {e}")
        return -1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "table_name,expected_count",
    [
        ("alignments", 4),
        ("armor", 1),
        ("attributes", 49),
        ("characters", 2),
        ("directions", 10),
        ("effects", 44),
        ("environments", 10),
        ("exits", 6),
        ("food_items", 7),
        ("items", 10),
        ("lightsource_items", 1),
        ("mob_types", 4),
        ("mobs", 21),
        ("monsters", 7),
        ("npcs", 12),
        ("player_classes", 16),
        ("player_races", 12),
        ("players", 1),
        ("roles", 3),
        ("rooms", 6),
        ("weapon_items", 1),
    ],
)
async def test_players_db_table(db_engine, table_name: str, expected_count: int):
    table_name = table_name.lower()
    expected_count = expected_count

    actual_count = await get_table_record_count_sqlalchemy(db_engine, table_name)

    assert actual_count == expected_count, (
        f"Expected {expected_count} records in table '{table_name}', but found {actual_count}"
    )

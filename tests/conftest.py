import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.config import test_settings
from db.database import Model
from alembic import command
from alembic.config import Config

from src.main import app


async_engine = create_async_engine(
    url=test_settings.TEST_DATABASE_URL_asyncpg,
    echo=True,
)

new_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

@pytest.fixture(scope='session')
async def apply_migrations():
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
    alembic_cfg = Config(alembic_cfg_path)
    alembic_cfg = Config("../alembic.ini")
    script_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'migrations'))
    alembic_cfg.set_main_option('script_location', script_location)

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(autouse=True, scope='session')
async def prepare_database(apply_migrations):
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/api") as ac:
        yield ac
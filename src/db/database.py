from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.config import settings

class Model(DeclarativeBase):
    __abstract__ = True 
    id: Mapped[int] = mapped_column(primary_key=True)


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

new_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

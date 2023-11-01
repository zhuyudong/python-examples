import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

# os.environ.get("DATABASE_URL") 可来自于 docker-compose.yml 中的环境变量
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    # NOTE: 本地：localhost，Docker environment: db_server
    "postgresql+asyncpg://postgres:postgres@db_server:5432/fastapi_sqlmodel_alembic",
)

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_NAME= os.getenv("DATABASE_NAME", "bloqit")
DATABASE_USER= os.getenv("DATABASE_USER", "bloqit")
DATABASE_PASSWORD= os.getenv("DATABASE_PASSWORD", "mypassword")
DATABASE_HOST= os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT= os.getenv("DATABASE_PORT", "5432")

engine = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session 
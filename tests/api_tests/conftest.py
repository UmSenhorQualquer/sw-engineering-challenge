from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from bloqit.main import app
from bloqit.database import get_session
from httpx import AsyncClient
# Create test database
TEST_DATABASE_URL = "sqlite+aiosqlite://"  # In-memory database



print(TEST_DATABASE_URL)
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    future=True
)



# Fixture for database session
@pytest.fixture(name="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

app.dependency_overrides[get_session] = session

@pytest.fixture(autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(name="client")
async def client():
    
    async with AsyncClient(app=app) as c:
        yield c

@pytest.fixture(name="test_data")
def test_data_fixture():
    # Load test data from JSON files
    data_dir = "./data"
    with open(os.path.join(data_dir, "bloqs.json")) as f:
        bloqs_data = json.load(f)
    with open(os.path.join(data_dir, "lockers.json")) as f:
        lockers_data = json.load(f)
    with open(os.path.join(data_dir, "rents.json")) as f:
        rents_data = json.load(f)
    
    return {
        "bloqs": bloqs_data,
        "lockers": lockers_data,
        "rents": rents_data
    } 

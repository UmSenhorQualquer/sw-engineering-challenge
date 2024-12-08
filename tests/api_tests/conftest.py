import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import json
import os

from bloqit.main import app
from bloqit.database import get_session

# Create test database
TEST_DATABASE_URL = "sqlite://"  # In-memory database
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
    SQLModel.metadata.drop_all(engine)

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

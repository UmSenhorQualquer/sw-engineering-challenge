import copy
import random
import pytest
from fastapi.testclient import TestClient

@pytest.fixture(name="test_bloq")
async def test_bloq_fixture(client, test_data):
    """Create a test bloq and return its data"""
    idx = random.randint(0, len(test_data["bloqs"]) - 1)
    bloq_data = test_data["bloqs"][idx]
    del bloq_data["id"]
    response = await client.post("/bloqs/", json=bloq_data)
    assert response.status_code == 200
    return bloq_data

@pytest.mark.asyncio
async def test_get_lockers(client, test_data, test_bloq):
    # Create test locker
    idx = random.randint(0, len(test_data["lockers"]) - 1)
    locker_data = test_data["lockers"][idx]
    response = await client.post("/lockers/", json=locker_data)
    assert response.status_code == 200
    
    # Get all lockers
    response = await client.get("/lockers/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == locker_data["id"]

@pytest.mark.asyncio
async def test_get_locker(client, test_data, test_bloq):
    # Create test locker
    idx = random.randint(0, len(test_data["lockers"]) - 1)
    locker_data = test_data["lockers"][idx]
    response = await client.post("/lockers/", json=locker_data)
    assert response.status_code == 200
    
    # Get specific locker
    response = await client.get(f"/lockers/{locker_data['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == locker_data["id"]
    
    # Test non-existent locker
    response = await client.get("/lockers/nonexistent")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_locker(client, test_data, test_bloq):
    # Create locker
    idx = random.randint(0, len(test_data["lockers"]) - 1)
    locker_data = test_data["lockers"][idx]
    del locker_data["id"]
    response = await client.post("/lockers/", json=locker_data)
    assert response.status_code == 200
    assert len(response.json()["id"])>=0
    assert response.json()["bloqId"] == locker_data["bloqId"]
    assert response.json()["status"] == locker_data["status"]
    assert response.json()["isOccupied"] == locker_data["isOccupied"]

@pytest.mark.asyncio
async def test_update_locker_status(client, test_data, test_bloq):
    # Create test locker
    idx = random.randint(0, len(test_data["lockers"]) - 1)
    locker_data = copy.deepcopy(test_data["lockers"][idx])
    del locker_data["id"]

    response = await client.post("/lockers/", json=locker_data)
    assert response.status_code == 200

    locker_data = response.json()
    locker_id = locker_data["id"]
    
    # Update locker status
    new_status = "OPEN"
    response = await client.put(f"/lockers/{locker_id}/status?status={new_status}")
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    
    # Test invalid status
    response = await client.put(f"/lockers/{locker_id}/status?status=INVALID")
    assert response.status_code == 422  # Validation error
    
    # Test non-existent locker
    response = await client.put("/lockers/nonexistent/status?status=OPEN")
    assert response.status_code == 404 
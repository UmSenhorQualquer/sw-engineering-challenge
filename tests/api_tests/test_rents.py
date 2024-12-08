import copy
import random
import pytest
from fastapi.testclient import TestClient

@pytest.fixture(name="test_locker")
def test_locker_fixture(client, test_data):
    """Create a test bloq and locker, return locker data"""
    # Create bloq first
    idx = random.randint(0, len(test_data["bloqs"]) - 1)
    bloq_data = copy.deepcopy(test_data["bloqs"][idx])
    del bloq_data["id"]

    response = client.post("/bloqs/", json=bloq_data)
    assert response.status_code == 200
    
    bloq_data = test_data["bloqs"][idx]

    # Create locker
    locker_data = test_data["lockers"][0]
    del locker_data["id"]
    response = client.post("/lockers/", json=locker_data)
    assert response.status_code == 200
    return locker_data

def test_get_rents(client, test_data, test_locker):
    # Create test rent
    idx = random.randint(0, len(test_data["rents"]) - 1)
    rent_data = test_data["rents"][idx]
    response = client.post("/rents/", json=rent_data)
    assert response.status_code == 200
    
    # Get all rents
    response = client.get("/rents/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == rent_data["id"]

def test_get_rent(client, test_data, test_locker):
    # Create test rent
    idx = random.randint(0, len(test_data["rents"]) - 1)
    rent_data = test_data["rents"][idx]
    response = client.post("/rents/", json=rent_data)
    assert response.status_code == 200
    
    # Get specific rent
    response = client.get(f"/rents/{rent_data['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == rent_data["id"]
    
    # Test non-existent rent
    response = client.get("/rents/nonexistent")
    assert response.status_code == 404

def test_create_rent(client, test_data, test_locker):
    # Create rent
    idx = random.randint(0, len(test_data["rents"]) - 1)
    rent_data = test_data["rents"][idx]
    del rent_data["id"] 
    del rent_data["lockerId"]
    response = client.post("/rents/", json=rent_data)
    assert response.status_code == 200
    assert len(response.json()["id"])>=0
    assert response.json()["weight"] == rent_data["weight"]
    assert response.json()["size"] == rent_data["size"]
    assert response.json()["status"] == rent_data["status"]

def test_update_rent_status(client, test_data, test_locker):
    # Create test rent
    idx = random.randint(0, len(test_data["rents"]) - 1)
    rent_data = test_data["rents"][idx]
    del rent_data["id"]
    response = client.post("/rents/", json=rent_data)
    assert response.status_code == 200

    rent_data = response.json()
    
    # Update rent status
    new_status = "WAITING_PICKUP"
    response = client.put(f"/rents/{rent_data['id']}/status?status={new_status}")
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    
    # Test invalid status
    response = client.put(f"/rents/{rent_data['id']}/status?status=INVALID")
    assert response.status_code == 422  # Validation error
    
    # Test non-existent rent
    response = client.put("/rents/nonexistent/status?status=WAITING_PICKUP")
    assert response.status_code == 404

def test_rent_lifecycle(client, test_data, test_locker):
    """Test the complete lifecycle of a rent"""
    # Create rent in CREATED status
    idx = random.randint(0, len(test_data["rents"]) - 1)
    rent_data = test_data["rents"][idx]
    rent_data["status"] = "CREATED"
    del rent_data["id"]
    response = client.post("/rents/", json=rent_data)
    assert response.status_code == 200
    rent_id = response.json()["id"]
    
    # Update to WAITING_DROPOFF
    response = client.put(f"/rents/{rent_id}/status?status=WAITING_DROPOFF")
    assert response.status_code == 200
    assert response.json()["status"] == "WAITING_DROPOFF"
    
    # Update to WAITING_PICKUP
    response = client.put(f"/rents/{rent_id}/status?status=WAITING_PICKUP")
    assert response.status_code == 200
    assert response.json()["status"] == "WAITING_PICKUP"
    
    # Finally update to DELIVERED
    response = client.put(f"/rents/{rent_id}/status?status=DELIVERED")
    assert response.status_code == 200
    assert response.json()["status"] == "DELIVERED" 
import random
import pytest
from fastapi.testclient import TestClient

def test_get_bloqs(client, test_data):
    # Create test bloq
    idx = random.randint(0, len(test_data["bloqs"]) - 1)
    bloq_data = test_data["bloqs"][idx]
    response = client.post("/bloqs/", json=bloq_data)
    assert response.status_code == 200
    
    # Get all bloqs
    response = client.get("/bloqs/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == bloq_data["id"]

def test_get_bloq(client, test_data):
    # Create test bloq
    idx = random.randint(0, len(test_data["bloqs"]) - 1)
    bloq_data = test_data["bloqs"][idx]
    response = client.post("/bloqs/", json=bloq_data)
    assert response.status_code == 200
    
    # Get specific bloq
    response = client.get(f"/bloqs/{bloq_data['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == bloq_data["id"]
    
    # Test non-existent bloq
    response = client.get("/bloqs/nonexistent")
    assert response.status_code == 404

def test_create_bloq(client, test_data):
    idx = random.randint(0, len(test_data["bloqs"]) - 1)
    bloq_data = test_data["bloqs"][idx]
    response = client.post("/bloqs/", json=bloq_data)
    del bloq_data["id"]
    assert response.status_code == 200
    assert len(response.json()["id"])>=0
    assert response.json()["title"] == bloq_data["title"]
    assert response.json()["address"] == bloq_data["address"] 
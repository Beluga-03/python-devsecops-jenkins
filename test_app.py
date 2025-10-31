import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["status"] == "running"

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

def test_get_single_task(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1

def test_get_nonexistent_task(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404

def test_add_task(client):
    new_task = {"task": "New Test Task"}
    response = client.post('/tasks', json=new_task)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["task"] == "New Test Task"

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
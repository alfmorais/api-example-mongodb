import mongomock
import pytest
from fastapi.testclient import TestClient

from src.app.main import app
from src.database.database import get_database


@pytest.fixture(scope="function")
def db_client():
    client = mongomock.MongoClient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def database(db_client):
    _database = db_client["users"]
    return _database


@pytest.fixture
def client(db_client, database):
    def override_database():
        yield database

    app.dependency_overrides[get_database] = override_database
    with TestClient(app) as test_client:
        return test_client

    app.dependency_overrides.clear()

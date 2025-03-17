from fastapi.testclient import TestClient
from sqlmodel import Session
from main import app
from service.constants import USER_ROLE_COLLECTOR, USERNAME_ALREADY_REGISTERED
from tests.conftest import createTestData

def authenticate(client:TestClient, session:Session, username:str, password:str):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    return response

def test_register_success(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Register a new user
    response = client.post(
        "/register",
        json={
            "username": "new_user",
            "password": "password123",
            "name": "New User",
            "phone": "1234567890",
            "userRole": USER_ROLE_COLLECTOR
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["username"] == "new_user"
    assert json_response["name"] == "New User"

def test_register_unauthorized(client: TestClient):
    # Attempt to register without authentication
    response = client.post(
        "/register",
        json={
            "username": "unauthorized_user",
            "password": "password123",
            "name": "Unauthorized User",
            "phone": "9876543210",
            "userRole": USER_ROLE_COLLECTOR
        },
    )
    assert response.status_code == 401

def test_register_missing_fields(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Attempt to register with missing fields
    response = client.post(
        "/register",
        json={
            "username": "incomplete_user",
            # Missing password, email, name, and phone
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422

def test_register_duplicate_username(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Register a user
    client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "password123",
            "name": "Duplicate User",
            "userRole": USER_ROLE_COLLECTOR,
            "phone": "1234567890"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Attempt to register the same username again
    response = client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "password123",
            "name": "Duplicate User 2",
            "phone": "0987654321",
            "userRole": USER_ROLE_COLLECTOR
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert USERNAME_ALREADY_REGISTERED in response.text
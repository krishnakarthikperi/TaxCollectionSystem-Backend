"""
Unit Tests for Assignment Endpoints

This module contains unit tests for the assignment-related endpoints in the application.
It uses FastAPI's TestClient to simulate HTTP requests and validate the responses.

Functions:
    authenticate(client: TestClient, session: Session, username: str, password: str):
        Authenticates a user and returns the response containing the access token.

    test_assignVolunteer_success(client: TestClient, session: Session):
        Tests the successful assignment of a collector to a house by an admin.

    test_assignVolunteer_invalid_user(client: TestClient, session: Session):
        Tests the assignment of a non-existent user to a house and ensures it returns a 400 Bad Request error.

    test_assignVolunteer_invalid_house(client: TestClient, session: Session):
        Tests the assignment of a valid user to a non-existent house and ensures it returns a 400 Bad Request error.

    test_assignVolunteer_unauthorized(client: TestClient):
        Tests the assignment of a collector to a house without authentication and ensures it returns a 401 Unauthorized error.
"""
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.conftest import createTestData


def authenticate(client:TestClient, session:Session, username:str, password:str):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    assert response.status_code == 200
    return response

def test_assignVolunteer_success(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Create a valid assignment
    response = client.post(
        "/assign-collector",
        json={
            "username": "collector",
            "houseId": "1"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["username"] == "collector"
    assert json_response["houseId"] == "1"

def test_assignVolunteer_invalid_user(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Attempt to assign a non-existent user
    response = client.post(
        "/assign-collector",
        json={
            "username": "nonexistent_user",
            "houseId": "1"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert "invalid volunteer details" in response.text.lower()

def test_assignVolunteer_invalid_house(client: TestClient, session: Session):
    # Authenticate as admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Attempt to assign a valid user to a non-existent house
    response = client.post(
        "/assign-collector",
        json={
            "username": "collector",
            "houseId": "nonexistent_house"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert "invalid house number" in response.text.lower()

def test_assignVolunteer_unauthorized(client: TestClient):
    # Attempt to assign without authentication
    response = client.post(
        "/assign-collector",
        json={
            "username": "collector",
            "houseId": "house123"
        },
    )
    assert response.status_code == 401
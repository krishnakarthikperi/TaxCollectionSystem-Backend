"""
This module contains test cases for user registration functionality in the Tax Collection system.
Functions:
    authenticate(client: TestClient, session: Session, username: str, password: str) -> Response:
        Authenticates a user and returns the response containing the access token.
    test_register_success(client: TestClient, session: Session):
        Tests successful registration of a new user with valid credentials and authorization.
    test_register_unauthorized(client: TestClient):
        Tests that registration fails with a 401 status code when attempted without authentication.
    test_register_missing_fields(client: TestClient, session: Session):
        Tests that registration fails with a 422 status code when required fields are missing in the request.
    test_register_duplicate_username(client: TestClient, session: Session):
        Tests that registration fails with a 400 status code when attempting to register a username that already exists.
"""

from fastapi.testclient import TestClient
from sqlmodel import Session
from main import app
from service.constants import USER_ROLE_COLLECTOR, USERNAME_ALREADY_REGISTERED
from tests.conftest import createTestData


def authenticate(
    client: TestClient,
    session: Session,
    username: str,
    password: str,
):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    return response


def test_register_success(
    client: TestClient,
    session: Session,
):
    """
    GIVEN an authenticated admin user with valid credentials
    WHEN the admin sends a POST request to the '/register' endpoint with valid user details
    THEN the response should have a status code of 200, and the returned JSON should contain the correct details of the newly registered user
    """
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


def test_register_unauthorized(
    client: TestClient,
):
    """
    GIVEN an unauthenticated user attempting to register
    WHEN the user sends a POST request to the '/register' endpoint with valid registration details
    THEN the server should respond with a 401 Unauthorized status code, indicating that authentication is required
    """
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


def test_register_missing_fields(
    client: TestClient,
    session: Session,
):
    """
    GIVEN an authenticated admin user
    WHEN a registration attempt is made with missing required fields
    THEN the server should respond with a 422 Unprocessable Entity status code
    """
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


def test_register_duplicate_username(
    client: TestClient,
    session: Session,
):
    """
    GIVEN an authenticated admin user and a registered user with a specific username,
    WHEN the admin attempts to register another user with the same username,
    THEN the server should respond with a 400 status code and an appropriate error message indicating
        that the username is already registered.
    """
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

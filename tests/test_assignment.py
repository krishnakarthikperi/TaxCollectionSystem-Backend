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

    def authenticate(
        client: TestClient, session: Session, username: str, password: str
    ):
        """
        Authenticate a user by creating test data and sending a POST request to obtain a token.
        Args:
            client (TestClient): The test client for making HTTP requests.
            session (Session): The database session for creating test data.
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            Response: The response object from the POST request containing the authentication token.
        """

    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    assert response.status_code == 200
    return response

def test_assignVolunteer_success(client: TestClient, session: Session):
    """
    GIVEN a TestClient instance and a database session, and an authenticated admin user,
    WHEN the admin assigns a collector to a house by sending a POST request to the '/assign-collector' endpoint
        with valid data and an authorization token,
    THEN the response should have a status code of 200, and the returned JSON should confirm the assignment
        with the correct 'username' and 'houseId'.
    """

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
    """
    GIVEN an authenticated admin user and a non-existent username,
    WHEN the admin attempts to assign the non-existent user as a collector to a house,
    THEN the server should respond with a 400 status code and an error message indicating invalid volunteer details.
    """

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
    """
    GIVEN an authenticated admin user and a valid collector username,
    WHEN the admin attempts to assign the collector to a non-existent house,
    THEN the API should respond with a 400 status code and an error message indicating an invalid house number.
    """
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
    """
    GIVEN an unauthenticated client attempting to assign a volunteer collector to a house,
    WHEN the client sends a POST request to the '/assign-collector' endpoint with the required payload,
    THEN the server should respond with a 401 Unauthorized status code, indicating that authentication is required.
    """
    # Attempt to assign without authentication
    response = client.post(
        "/assign-collector",
        json={
            "username": "collector",
            "houseId": "house123"
        },
    )
    assert response.status_code == 401

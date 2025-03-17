"""
Unit Tests for House Endpoints

This module contains unit tests for the house-related endpoints in the application.
It uses FastAPI's TestClient to simulate HTTP requests and validate the responses.

Functions:
    test_login(client: TestClient, session: Session):
        Tests the login endpoint to ensure it returns a valid access token and token type.

    test_createHouse(client: TestClient, session: Session):
        Tests the creation of a single house and validates the response.

    test_getHouseByHouseNumber(client: TestClient, session: Session):
        Tests retrieving a house by its house number and validates the response.

    test_getHouses(client: TestClient, session: Session):
        Tests retrieving all houses and validates the response.

    test_createHouses_success(client: TestClient, session: Session):
        Tests the creation of multiple houses with valid data and validates the response.

    test_createHouses_unauthorized(client: TestClient, session: Session):
        Tests the creation of houses without authentication and ensures it returns a 401 Unauthorized error.

    test_createHouses_invalid_data(client: TestClient, session: Session):
        Tests the creation of houses with invalid data and ensures it returns a 422 Unprocessable Entity error.
"""

from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from auth.authcheck import hashPassword
from main import app
from tests.conftest import createTestData


def authenticate(
    client: TestClient,
    session: Session,
    username: str,
    password: str,
):
    """
    Authenticates a user by sending a POST request to the /token endpoint with the provided credentials.

    Args:
        client (TestClient): The test client used to send HTTP requests.
        session (Session): The database session used to create test data.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        Response: The response object from the POST request to the /token endpoint.
    """
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    return response


def test_login(
    client: TestClient,
    session: Session,
):
    """
    GIVEN a TestClient instance and a database session
    WHEN the authenticate function is called with valid credentials (username="admin", password="admin")
    THEN the response should have a status code of 200, contain an "access_token" in the JSON response,
        and the "token_type" should be "Bearer".
    """
    response = authenticate(client=client, session=session, username="admin", password="admin")
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "Bearer"


def test_createHouse(
    client: TestClient,
    session: Session,
):
    def test_createHouse(client: TestClient, session: Session):
        """
        GIVEN a valid authenticated user with the necessary permissions
              and a valid payload for creating a house record.
        WHEN the user sends a POST request to the '/house' endpoint with the payload
             and a valid access token in the Authorization header.
        THEN the server should respond with a status code of 200,
             and the response should contain the created house record with the correct details.
        """

    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    response = client.post(
        "/house",
        json=[
            {
                "assessmentNumber": 3,
                "houseNumber": "3",
                "houseValue": 1000000.0,
                "houseTax": 10000.0,
                "waterTax": 1000.0,
                "libraryTax": 100.0,
                "lightingTax": 100.0,
                "drianageTax": 100.0,
                "husbandOrFatherNameOfOwner": "John Doe III",
                "ownerName": "Jane Doe III"
            }
        ],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 1
    json_response = json_response[0]
    assert json_response["assessmentNumber"] == 3
    assert json_response["houseNumber"] == "3"
    assert json_response["houseValue"] == 1000000.0
    assert json_response["houseTax"] == 10000.0
    assert json_response["waterTax"] == 1000.0
    assert json_response["libraryTax"] == 100.0
    assert json_response["lightingTax"] == 100.0
    assert json_response["drianageTax"] == 100.0
    assert json_response["husbandOrFatherNameOfOwner"] == "John Doe III"
    assert json_response["ownerName"] == "Jane Doe III"


def test_getHouseByHouseNumber(
    client: TestClient,
    session: Session,
):
    """
    Test the `getHouseByHouseNumber` endpoint.

    GIVEN a valid TestClient and database session, and an authenticated user with the username "admin" and password "admin",
    WHEN the user sends a GET request to the `/households/1` endpoint with a valid access token,
    THEN the response should have a status code of 200, and the JSON response should contain the details of the house with:
        - assessmentNumber: 1
        - houseNumber: "1"
        - houseValue: 1000000.0
        - houseTax: 10000.0
        - waterTax: 1000.0
        - libraryTax: 100.0
        - lightingTax: 100.0
        - drianageTax: 100.0
        - husbandOrFatherNameOfOwner: "John Doe"
        - ownerName: "Jane Doe"
    """
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    response = client.get(
        "/households/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 1
    json_response = json_response[0]
    assert json_response["assessmentNumber"] == 1
    assert json_response["houseNumber"] == "1"
    assert json_response["houseValue"] == 1000000.0
    assert json_response["houseTax"] == 10000.0
    assert json_response["waterTax"] == 1000.0
    assert json_response["libraryTax"] == 100.0
    assert json_response["lightingTax"] == 100.0
    assert json_response["drianageTax"] == 100.0
    assert json_response["husbandOrFatherNameOfOwner"] == "John Doe"
    assert json_response["ownerName"] == "Jane Doe"    


def test_getHouses(
    client: TestClient,
    session: Session,
):
    """
    Test the `GET /households` endpoint.

    GIVEN a valid authenticated user with the necessary permissions
    WHEN the user sends a GET request to the `/households` endpoint
    THEN the response should return a status code of 200 and a list of households with the correct details,
        including assessment number, house number, house value, taxes, and owner information.
    """
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    response = client.get(
        "/households",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2
    json_response = json_response[0]
    assert json_response["assessmentNumber"] == 1
    assert json_response["houseNumber"] == "1"
    assert json_response["houseValue"] == 1000000.0
    assert json_response["houseTax"] == 10000.0
    assert json_response["waterTax"] == 1000.0
    assert json_response["libraryTax"] == 100.0
    assert json_response["lightingTax"] == 100.0
    assert json_response["drianageTax"] == 100.0
    assert json_response["husbandOrFatherNameOfOwner"] == "John Doe"
    assert json_response["ownerName"] == "Jane Doe"    


def test_createHouses_success(
    client: TestClient,
    session: Session,
):
    """
    GIVEN a TestClient and a database session with an authenticated user
    WHEN the client sends a POST request to the '/house' endpoint with a list of house details
        and a valid access token in the headers
    THEN the server should respond with a 200 status code and return a JSON response containing
        the details of the created houses, matching the input data.
    """
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    response = client.post(
        "/house",
        json=[
            {
                "assessmentNumber": 4,
                "houseNumber": "4",
                "houseValue": 1500000.0,
                "houseTax": 15000.0,
                "waterTax": 1500.0,
                "libraryTax": 150.0,
                "lightingTax": 150.0,
                "drianageTax": 150.0,
                "husbandOrFatherNameOfOwner": "John Doe IV",
                "ownerName": "Jane Doe IV"
            },
            {
                "assessmentNumber": 5,
                "houseNumber": "5",
                "houseValue": 2500000.0,
                "houseTax": 25000.0,
                "waterTax": 2500.0,
                "libraryTax": 250.0,
                "lightingTax": 250.0,
                "drianageTax": 250.0,
                "husbandOrFatherNameOfOwner": "John Doe V",
                "ownerName": "Jane Doe V"
            }
        ],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2
    assert json_response[0]["assessmentNumber"] == 4
    assert json_response[0]["houseNumber"] == "4"
    assert json_response[1]["assessmentNumber"] == 5
    assert json_response[1]["houseNumber"] == "5"


def test_createHouses_unauthorized(
    client: TestClient,
    session: Session,
):
    """
    GIVEN an unauthorized client and a database session,
    WHEN the client attempts to create a house entry by sending a POST request to the "/house" endpoint,
    THEN the server should respond with a 401 Unauthorized status code, indicating that the client is not authorized to perform this action.
    """
    response = client.post(
        "/house",
        json=[
            {
                "assessmentNumber": 6,
                "houseNumber": "6",
                "houseValue": 3000000.0,
                "houseTax": 30000.0,
                "waterTax": 3000.0,
                "libraryTax": 300.0,
                "lightingTax": 300.0,
                "drianageTax": 300.0,
                "husbandOrFatherNameOfOwner": "John Doe VI",
                "ownerName": "Jane Doe VI"
            }
        ],
    )
    assert response.status_code == 401


def test_createHouses_invalid_data(
    client: TestClient,
    session: Session,
):
    """
    GIVEN a TestClient and a database session with an authenticated user
    WHEN a POST request is made to the '/house' endpoint with invalid data
        (e.g., an invalid data type for the 'assessmentNumber' field)
    THEN the server should respond with a 422 Unprocessable Entity status code,
         indicating that the input validation has failed.
    """
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    response = client.post(
        "/house",
        json=[
            {
                "assessmentNumber": "invalid",  # Invalid data type
                "houseNumber": "7",
                "houseValue": 3500000.0,
                "houseTax": 35000.0,
                "waterTax": 3500.0,
                "libraryTax": 350.0,
                "lightingTax": 350.0,
                "drianageTax": 350.0,
                "husbandOrFatherNameOfOwner": "John Doe VII",
                "ownerName": "Jane Doe VII"
            }
        ],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422

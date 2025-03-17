"""
Unit Tests for Authentication Endpoints

This module contains unit tests for the authentication-related endpoints in the application.
It uses FastAPI's TestClient to simulate HTTP requests and validate the responses.

Functions:
    test_login():
        Tests the login endpoint to ensure it returns a valid access token and token type.

    test_refresh_token_success():
        Tests the refresh token endpoint with a valid refresh token to ensure it generates a new access token.

    test_refresh_token_invalid():
        Tests the refresh token endpoint with an invalid refresh token to ensure it returns a 401 Unauthorized error.

    test_refresh_token_missing():
        Tests the refresh token endpoint without providing a refresh token to ensure it returns a 422 Unprocessable Entity error.

    test_logout_success():
        Tests the logout endpoint with a valid access token to ensure it logs out successfully.

    test_logout_invalid_token():
        Tests the logout endpoint with an invalid access token to ensure it returns a 401 Unauthorized error.

    test_logout_missing_token():
        Tests the logout endpoint without providing an access token to ensure it returns a 401 Unauthorized error.
"""

from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session
from main import app
from tests.conftest import createTestData

# client = TestClient(app)
def authenticate(client:TestClient, session:Session, username:str, password:str):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    return response

def test_login(client:TestClient, session:Session):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin", "grant_type": "password"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "Bearer"

def test_refresh_token_success(client:TestClient, session:Session):
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    response = client.post(
        "/token/refresh",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "Bearer"
    assert json_response["access_token"] != access_token


def test_refresh_token_invalid(client:TestClient, session:Session):
    createTestData(session)
    # Use an invalid refresh token
    response = client.post(
        "/token/refresh", json={"refresh_token": "invalid_refresh_token"}
    )
    json_response = response.json()
    assert response.status_code == 401
    assert json_response["detail"] == "Could not validate credentials" #Change the exception


def test_refresh_token_missing(client:TestClient, session:Session):
    createTestData(session)
    # Missing refresh token
    response = client.post("/token/refresh", json={})
    assert response.status_code == 422
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "Field required"


def test_logout_success(client:TestClient, session:Session):
    # First, login to get the access token
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Use the access token to logout
    response = client.post(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == "Logged out successfully"


def test_logout_invalid_token(client:TestClient, session:Session):
    createTestData(session)
    # Attempt to logout with an invalid token
    response = client.post(
        "/logout", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Could not validate credentials"


def test_logout_missing_token(client:TestClient, session:Session):
    createTestData(session)
    # Attempt to logout without providing a token
    response = client.post("/logout")
    assert response.status_code == 401
    json_response = response.json()
    assert json_response["detail"] == "Not authenticated"

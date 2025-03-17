"""
Unit Tests for Tax Record Endpoints

This module contains unit tests for the tax record-related endpoints in the application.
It uses FastAPI's TestClient to simulate HTTP requests and validate the responses.

Functions:
    authenticate(client: TestClient, session: Session, username: str, password: str):
        Authenticates a user and returns the response containing the access token.

    test_insertTaxRecord_success(client: TestClient, session: Session):
        Tests the successful insertion of a tax record by an authorized collector.

    test_insertTaxRecord_unauthorized(client: TestClient):
        Tests the insertion of a tax record without authentication and ensures it returns a 401 Unauthorized error.

    test_insertTaxRecord_forbidden(client: TestClient, session: Session):
        Tests the insertion of a tax record by a collector not assigned to the household and ensures it returns a 403 Forbidden error.

    test_getTaxRecords_success(client: TestClient, session: Session):
        Tests retrieving all tax records as an authenticated user and validates the response.

    test_admin_updateTaxRecordById_success(client: TestClient, session: Session):
        Tests the successful update of a tax record by an admin.

    test_assignedcollector_updateTaxRecordById_success(client: TestClient, session: Session):
        Tests the successful update of a tax record by a collector assigned to the household.

    test_unassignedcollector_updateTaxRecordById_success(client: TestClient, session: Session):
        Tests the update of a tax record by a collector not assigned to the household and ensures it returns a 401 Unauthorized error.

    test_updateTaxRecordById_not_found(client: TestClient, session: Session):
        Tests the update of a non-existent tax record and ensures it returns a 404 Not Found error.
"""

from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlmodel import Session

from service import constants
from service.constants import USER_ROLE_COLLECTOR
from tests.conftest import createTestData, createUserData


def authenticate(client:TestClient, session:Session, username:str, password:str):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    assert response.status_code == 200
    return response


def test_insertTaxRecord_success(client: TestClient, session: Session):
    # Authenticate as a collector
    response = authenticate(client=client, session=session, username="collector", password="collector")
    access_token = response.json()["access_token"]

    # Insert a tax record
    response = client.post(
        "/recordcollections",
        json=[
            {
                "houseId": "1",
                "collectorId": "collector",
                "amount": 5000.0,
            }
        ],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 1
    json_response = json_response[0]
    assert json_response["houseId"] == "1"
    assert json_response["amount"] == 5000.0


def test_insertTaxRecord_unauthorized(client: TestClient):
    # Attempt to insert a tax record without authentication
    response = client.post(
        "/recordcollections",
        json=[
            {
                "houseId": "1",
                "collectorId": "collector",
                "date": datetime.now(timezone.utc).isoformat(),
                "amount": 5000.0,
            }
        ],
    )
    assert response.status_code == 401

def test_insertTaxRecord_forbidden(client: TestClient, session: Session):
    # Authenticate as a non-collector user
    newCollector = createUserData(username="collector2", password="collector2", name="C2", userRole=USER_ROLE_COLLECTOR, phone=1234567890)
    session.add(newCollector)
    session.commit()
    response = authenticate(client=client, session=session, username=newCollector.username, password="collector2")
    access_token = response.json()["access_token"]

    # Attempt to insert a tax record
    response = client.post(
        "/recordcollections",
        json=[
            {
                "houseId": "1",
                "collectorId": "collector",
                "date": datetime.now(timezone.utc).isoformat(),
                "amount": 5000.0,
            }
        ],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403
    assert constants.INCORRECT_HOUSE_MAPPING in response.text

def test_getTaxRecords_success(client: TestClient, session: Session):
    # Authenticate as a user
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Get tax records
    response = client.get(
        "/gettaxrecords",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_updateTaxRecordById_success(client: TestClient, session: Session):
    # Authenticate as an admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Update a tax record
    response = client.put(
        "/tax-record/1",
        json={
            "amount": 6000.0
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["amount"] == 6000.0

def test_assignedcollector_updateTaxRecordById_success(client: TestClient, session: Session):
    # Authenticate as an assigned collector
    response = authenticate(client=client, session=session, username="collector", password="collector")
    access_token = response.json()["access_token"]

    # Update a tax record
    response = client.put(
        "/tax-record/1",
        json={
            "amount": 6000.0
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["amount"] == 6000.0

def test_unassignedcollector_updateTaxRecordById_success(client: TestClient, session: Session):
    # Authenticate as an unassigned collector
    newCollector = createUserData(username="collector2", password="collector2", name="C2", userRole=USER_ROLE_COLLECTOR, phone=1234567890)
    session.add(newCollector)
    session.commit()
    response = authenticate(client=client, session=session, username=newCollector.username, password="collector2")
    access_token = response.json()["access_token"]

    # Update a tax record
    response = client.put(
        "/tax-record/1",
        json={
            "amount": 6000.0
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401

def test_updateTaxRecordById_not_found(client: TestClient, session: Session):
    # Authenticate as an admin
    response = authenticate(client=client, session=session, username="admin", password="admin")
    access_token = response.json()["access_token"]

    # Attempt to update a non-existent tax record
    response = client.put(
        "/tax-record/999",
        json={
            "amount": 6000.0,
            "taxType": "Updated Tax",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert "record not found" in response.text.lower()
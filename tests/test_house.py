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
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from auth.authcheck import hashPassword
from main import app
from db import getSession

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[getSession] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def createTestData(session: Session):
    from objects.house import House
    house1 = House(
        assessmentNumber=1,
        houseNumber="1",
        houseValue=1000000.0,
        houseTax=10000.0,
        waterTax=1000.0,
        libraryTax=100.0,
        lightingTax=100.0,
        drianageTax=100.0,
        husbandOrFatherNameOfOwner="John Doe",
        ownerName="Jane Doe"
    )
    house2 = House(
        assessmentNumber=2,
        houseNumber="2",
        houseValue=2000000.0,
        houseTax=20000.0,
        waterTax=2000.0,
        libraryTax=200.0,
        lightingTax=200.0,
        drianageTax=200.0,
        husbandOrFatherNameOfOwner="John Doe II",
        ownerName="Jane Doe II"
    )
    session.add_all([house1, house2])
    session.commit()
    # Verify data creation
    # print("Houses in DB:", session.query(House).all())

    # Create User
    from objects.user import User
    adminUser = User(
        username="admin",
        password=hashPassword("admin"),
        name="Admin",
        userRole="admin",
        phone=1234567890
    )
    collectorUser = User(
        username="collector",
        password=hashPassword("collector"),
        name="Collector",
        userRole="collector",
        phone=1234567890
    )
    session.add_all([adminUser, collectorUser])
    session.commit()

    #Create Assignment
    from objects.assignment import Assignment
    assignment1 = Assignment(
        houseId=1,
        username="collector"
    )
    session.add(assignment1)
    session.commit()

    #Create Taxrecord
    from objects.taxrecord import TaxRecord
    taxRecord1 = TaxRecord(
        amount=1000.0,
        houseId=1,
        collectorId="collector",
        date=datetime.now(timezone.utc)
    )
    session.add(taxRecord1)
    session.commit()

def authenticate(client:TestClient, session:Session, username:str, password:str):
    createTestData(session)
    response = client.post(
        "/token",
        data={"username": username, "password": password, "grant_type": "password"},
    )
    return response

def test_login(client:TestClient, session:Session):
    response = authenticate(client=client, session=session, username="admin", password="admin")
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "Bearer"

def test_createHouse(client:TestClient,session:Session):
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

def test_getHouseByHouseNumber(client:TestClient,session:Session):
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

def test_getHouses(client:TestClient,session:Session):
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

def test_createHouses_success(client: TestClient, session: Session):
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

def test_createHouses_unauthorized(client: TestClient, session: Session):
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

def test_createHouses_invalid_data(client: TestClient, session: Session):
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
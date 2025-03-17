"""
This module contains pytest fixtures and helper functions for setting up test data
and dependencies for the Tax Collection application.
Fixtures:
    - session_fixture: Creates an in-memory SQLite database session for testing.
    - client_fixture: Provides a FastAPI TestClient with overridden dependencies.
Helper Functions:
    - createTestData(session): Populates the database with test data including houses,
      users, assignments, and tax records.
    - createHouse(assessmentNumber, houseNumber, houseValue, houseTax, waterTax,
      libraryTax, lightingTax, drianageTax, husbandOrFatherNameOfOwner, ownerName):
      Creates a House object with the specified attributes.
    - createAssignment(houseId, username): Creates an Assignment object linking a
      house to a user.
    - createUserData(username, password, name, userRole, phone): Creates a User object
      with hashed password and specified attributes.
    - createTaxRecord(amount, houseId, collectorId, date): Creates a TaxRecord object
      with the specified attributes.
Dependencies:
    - Uses FastAPI's dependency injection to override the database session during tests.
    - Relies on SQLModel for ORM functionality and SQLite for in-memory testing.
"""

from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from auth.authcheck import hashPassword
from main import app
from db import getSession
from service.constants import USER_ROLE_ADMIN, USER_ROLE_COLLECTOR
from objects.taxrecord import TaxRecord
from objects.assignment import Assignment
from objects.user import User
from objects.house import House

@pytest.fixture(name="session")
def session_fixture():
    """
    Creates a session fixture for testing purposes using an in-memory SQLite database.

    This fixture sets up an SQLite database with `check_same_thread` set to False
    and uses a `StaticPool` to ensure the database persists for the duration of the tests.
    It initializes the database schema using SQLModel metadata and provides a session
    for interacting with the database.

    Yields:
        Session: A SQLAlchemy session connected to the in-memory SQLite database.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(
        engine,
    )
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    A fixture that provides a test client for the application with a session override.
    This fixture sets up a dependency override for the `getSession` function to use
    the provided `session` object. It then creates a `TestClient` instance for the
    application (`app`) and yields it for use in tests. After the test is complete,
    the dependency overrides are cleared to restore the application's original state.
    Args:
        session (Session): The database session to be used as an override for the
                           application's `getSession` dependency.
    Yields:
        TestClient: A test client instance configured with the overridden session.
    """
    def get_session_override():
        return session

    app.dependency_overrides[getSession] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def createTestData(session: Session):
    """
    Populate the database session with test data for houses, users, assignments,
    and tax records.
    Args:
        session (Session): The database session to which the test data will be added.
    Test Data Created:
        1. Houses:
            - House 1: Assessment number 1, value 1,000,000.0, taxes (house: 10,000.0,
              water: 1,000.0, library: 100.0, lighting: 100.0, drainage: 100.0),
              owner: Jane Doe, husband/father: John Doe.
            - House 2: Assessment number 2, value 2,000,000.0, taxes (house: 20,000.0,
              water: 2,000.0, library: 200.0, lighting: 200.0, drainage: 200.0),
              owner: Jane Doe II, husband/father: John Doe II.
        2. Users:
            - Admin user: Username "admin", password "admin", role "admin,collector",
              phone 1234567890.
            - Collector user: Username "collector", password "collector", role "collector",
              phone 1234567890.
        3. Assignments:
            - Assignment 1: House ID 1 assigned to the collector user.
        4. Tax Records:
            - Tax record 1: Amount 1,000.0, house ID 1, collected by "collector",
              date set to the current UTC time.
    Note:
        This function commits the changes to the database session after adding all
        the test data.
    """
    house1 = createHouse(
        assessmentNumber=1,
        houseNumber="1",
        houseValue=1000000.0,
        houseTax=10000.0,
        waterTax=1000.0,
        libraryTax=100.0,
        lightingTax=100.0,
        drianageTax=100.0,
        husbandOrFatherNameOfOwner="John Doe",
        ownerName="Jane Doe",
    )
    house2 = createHouse(
        assessmentNumber=2,
        houseNumber="2",
        houseValue=2000000.0,
        houseTax=20000.0,
        waterTax=2000.0,
        libraryTax=200.0,
        lightingTax=200.0,
        drianageTax=200.0,
        husbandOrFatherNameOfOwner="John Doe II",
        ownerName="Jane Doe II",
    )
    session.add_all(
        [house1, house2],
    )
    session.flush()

    # Create User
    adminUser = createUserData(
        username="admin",
        password="admin",
        name="Admin",
        userRole=",".join([USER_ROLE_ADMIN, USER_ROLE_COLLECTOR]),
        phone=1234567890,
    )

    collectorUser = createUserData(
        username="collector",
        password="collector",
        name="Collector",
        userRole=USER_ROLE_COLLECTOR,
        phone=1234567890,
    )
    session.add_all(
        [adminUser, collectorUser],
    )
    session.flush()

    # Create Assignment
    assignment1 = createAssignment(
        houseId="1",
        username="collector",
    )
    session.add(
        assignment1,
    )
    session.flush()

    # Create Taxrecord
    taxRecord1 = createTaxRecord(
        amount=1000.0,
        houseId=1,
        collectorId="collector",
        date=datetime.now(
            timezone.utc,
        ),
    )
    session.add(
        taxRecord1,
    )
    session.commit()


def createHouse(
    assessmentNumber: int,
    houseNumber: str,
    houseValue: float,
    houseTax: float,
    waterTax: float,
    libraryTax: float,
    lightingTax: float,
    drianageTax: float,
    husbandOrFatherNameOfOwner: str,
    ownerName: str,
):
    """
    Creates a House object with the specified attributes.

    Args:
        assessmentNumber (int): The unique assessment number of the house.
        houseNumber (str): The house number or identifier.
        houseValue (float): The monetary value of the house.
        houseTax (float): The tax amount for the house.
        waterTax (float): The tax amount for water usage.
        libraryTax (float): The tax amount for library services.
        lightingTax (float): The tax amount for lighting services.
        drianageTax (float): The tax amount for drainage services.
        husbandOrFatherNameOfOwner (str): The name of the husband or father of the house owner.
        ownerName (str): The name of the house owner.

    Returns:
        House: An instance of the House object with the specified attributes.
    """
    return House(
        assessmentNumber=assessmentNumber,
        houseNumber=houseNumber,
        houseValue=houseValue,
        houseTax=houseTax,
        waterTax=waterTax,
        libraryTax=libraryTax,
        lightingTax=lightingTax,
        drianageTax=drianageTax,
        husbandOrFatherNameOfOwner=husbandOrFatherNameOfOwner,
        ownerName=ownerName,
    )


def createAssignment(
    houseId: str,
    username: str,
):
    """
    Creates an Assignment object with the given house ID and username.

    Args:
        houseId (str): The unique identifier for the house.
        username (str): The username associated with the assignment.

    Returns:
        Assignment: An instance of the Assignment class initialized with the provided house ID and username.
    """
    return Assignment(
        houseId=houseId,
        username=username,
    )


def createUserData(
    username: str,
    password: str,
    name: str,
    userRole: str,
    phone: int,
):
    def createUserData(
        username: str, password: str, name: str, userRole: str, phone: int
    ):
        """
        Creates a User object with the provided user details.

        Args:
            username (str): The username of the user.
            password (str): The plaintext password of the user, which will be hashed.
            name (str): The full name of the user.
            userRole (str): The role assigned to the user (e.g., admin, user).
            phone (int): The phone number of the user.

        Returns:
            User: An instance of the User class with the provided details.
        """

    return User(
        username=username,
        password=hashPassword(password),
        name=name,
        userRole=userRole,
        phone=phone,
    )


def createTaxRecord(
    amount: float,
    houseId: int,
    collectorId: str,
    date: datetime = datetime.now(timezone.utc).isoformat(),
):
    """
    Creates a TaxRecord instance with the specified details.

    Args:
        amount (float): The amount of tax collected.
        houseId (int): The unique identifier of the house.
        collectorId (str): The unique identifier of the tax collector.
        date (datetime, optional): The date and time of tax collection in ISO 8601 format.
            Defaults to the current UTC time.

    Returns:
        TaxRecord: An instance of the TaxRecord class containing the provided details.
    """
    return TaxRecord(
        amount=amount,
        houseId=houseId,
        collectorId=collectorId,
        date=date,
    )

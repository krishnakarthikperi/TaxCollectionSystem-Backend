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
        ownerName="Jane Doe"
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
        ownerName="Jane Doe II"
    )
    session.add_all([house1, house2])
    session.flush()

    # Create User
    adminUser = createUserData(
        username="admin",
        password="admin",
        name="Admin",
        userRole=','.join([USER_ROLE_ADMIN,USER_ROLE_COLLECTOR]),
        phone=1234567890
    )

    collectorUser = createUserData(
        username="collector",
        password="collector",
        name="Collector",
        userRole=USER_ROLE_COLLECTOR,
        phone=1234567890
    )
    session.add_all([adminUser, collectorUser])
    session.flush()

    #Create Assignment
    assignment1 = createAssignment(
        houseId="1",
        username="collector"
    )
    session.add(assignment1)
    session.flush()

    #Create Taxrecord
    taxRecord1 = createTaxRecord(
        amount=1000.0,
        houseId=1,
        collectorId="collector",
        date=datetime.now(timezone.utc)
    )
    session.add(taxRecord1)
    session.commit()

def createHouse(assessmentNumber: int, houseNumber: str, houseValue: float, houseTax: float, waterTax: float, libraryTax: float, lightingTax: float, drianageTax: float, husbandOrFatherNameOfOwner: str, ownerName: str):
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
        ownerName=ownerName
    )

def createAssignment(houseId: str, username: str):
    return Assignment(
        houseId=houseId,
        username=username
    )

def createUserData(username: str, password: str, name: str, userRole: str, phone: int):
    return User(
        username=username,
        password=hashPassword(password),
        name=name,
        userRole=userRole,
        phone=phone
    )

def createTaxRecord(amount: float, houseId: int, collectorId: str, date: datetime=datetime.now(timezone.utc).isoformat()):
    return TaxRecord(
        amount=amount,
        houseId=houseId,
        collectorId=collectorId,
        date=date
    )
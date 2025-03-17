"""
This module defines the FastAPI routes for managing house-related operations.
Routes:
    - POST /house:
        Creates new house records in the database.
        Request Body: List of HousePOSTRequest objects.
        Response: List of created HousePOSTRequest objects.
        Dependencies: Requires authentication via `getCurrentUser`.
    - GET /households:
        Retrieves all house records from the database.
        Response: List of HouseGETResponse objects.
        Dependencies: Requires authentication via `getCurrentUser`.
    - GET /households/{household_id}:
        Retrieves house records by a specific household ID.
        Path Parameter: `household_id` (str) - The ID of the household to filter by.
        Response: List of HouseGETResponse objects.
        Dependencies: Requires authentication via `getCurrentUser`.
Dependencies:
    - `getCurrentUser`: Ensures the user is authenticated.
    - `getSession`: Provides a database session for interacting with the database.
Modules:
    - `controller.house`: Contains the business logic for house-related operations.
    - `objects.house`: Defines the data models for house-related requests and responses.
    - `auth.auth`: Provides authentication utilities.
    - `db`: Provides database session management.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.house as controller
from db import getSession
from objects.house import House, HouseGETRequest, HouseGETResponse, HousePOSTRequest

router = APIRouter()


@router.post(
    "/house",
    response_model=List[HousePOSTRequest],
    dependencies=[Depends(getCurrentUser)],
)
def createHouses(
        houses: List[HousePOSTRequest],
        db: Session = Depends(getSession)
):
    """
    Creates new house records in the database.

    Args:
        houses (List[HousePOSTRequest]): A list of house data objects to be created.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.

    Returns:
        List[House]: A list of newly created house objects.
    """
    newHouses = [House(**house.model_dump()) for house in houses]
    return controller.createHouses(
        houses=newHouses,
        db=db,
    )


@router.get(
    "/households",
    response_model=List[HouseGETResponse],
    dependencies=[Depends(getCurrentUser)],
)
def getHouses(
    db: Session = Depends(getSession)
):
    """
    Fetches a list of houses from the database.

    Args:
        db (Session): The database session dependency, provided by FastAPI's Depends.

    Returns:
        List[House]: A list of house objects retrieved from the database.
    """
    return controller.getHouses(db=db)


@router.get(
    "/households/{household_id}",
    response_model=List[HouseGETResponse],
    dependencies=[Depends(getCurrentUser)],
)
def getHousesByHouseNumber(
    household_id: str,
    db: Session = Depends(getSession)
):
    """
    Retrieve houses based on a given household ID.
    Args:
        household_id (str): The ID of the household to retrieve houses for.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.
    Returns:
        List[House]: A list of houses that match the given household ID.
    """

    houses = [HouseGETRequest(houseNumber=household_id)]
    houseNumbers = [house.houseNumber for house in houses]
    return controller.getHousesByHouseNumbers(
        houseNumbers=houseNumbers,
        db=db,
    )

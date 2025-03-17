"""
This module provides functionality for managing houses, including creating houses,
retrieving houses, and parsing house data into response objects.
Classes:
    None
Functions:
    createHouses(houses: List[HousePOSTRequest], db: Session = Depends(getSession)) -> List[HouseGETResponse]:
        Creates new house records in the database and retrieves the created houses.
    getHouses(db: Session = Depends(getSession)) -> List[HouseGETResponse]:
        Retrieves all houses along with their associated tax records, assignments, and users.
    getHousesByHouseNumbers(houseNumbers: List[str], db: Session = Depends(getSession)) -> List[HouseGETResponse]:
        Retrieves houses by their house numbers along with their associated tax records, assignments, and users.
    parseHouseGETResponse(results: any) -> List[HouseGETResponse]:
        Parses raw database query results into a list of `HouseGETResponse` objects.
Constants:
    ADMIN_ROLE: str
        Represents the role of an admin user.
    STANDARD_ROLE: str
        Represents the role of a standard user.
"""

from typing import List
from fastapi import Depends
from sqlmodel import Session, select
from db import SessionDep, getSession
from objects.assignment import Assignment, AssignmentGETRequest
from objects.house import House, HousePOSTRequest, HouseGETRequest, HouseGETResponse
from objects.taxrecord import TaxRecord, TaxRecordGETResponse
from objects.user import User, UserGetResponse

ADMIN_ROLE = "ADMIN"
STANDARD_ROLE = "STANDARD_USER"


def createHouses(
    houses: List[HousePOSTRequest],
    db: Session = Depends(getSession),
):
    """
    Creates multiple house records in the database.
    Args:
        houses (List[HousePOSTRequest]): A list of house data objects to be created.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.
    Returns:
        List[House]: A list of house objects retrieved from the database after creation.
    """

    houseNumbers = [house.houseNumber for house in houses]
    db.add_all(houses)
    db.commit()
    houses = getHousesByHouseNumbers(houseNumbers=houseNumbers, db=db)
    return houses


def getHouses(
    db: Session = Depends(getSession),
):
    """
    Fetches a list of houses along with their associated tax records, assignments, and user information.
    This function queries the database to retrieve data from the `House`, `TaxRecord`, `Assignment`,
    and `User` tables using outer joins. The results are then parsed into a response format.
    Args:
        db (Session): The database session dependency, provided by FastAPI's `Depends`.
    Returns:
        list: A parsed response containing the details of houses, their tax records, assignments,
        and associated users.
    """

    results = db.exec(
        select(House,TaxRecord,Assignment,User)
        .outerjoin(TaxRecord, TaxRecord.houseId == House.houseNumber)
        .outerjoin(Assignment, Assignment.houseId == House.houseNumber)
        .outerjoin(User, User.username == Assignment.username)
    ).all()
    return parseHouseGETResponse(results)


def getHousesByHouseNumbers(
    houseNumbers: List[str],
    db: Session = Depends(getSession),
):
    """
    Retrieve house details along with related tax records, assignments,
    and user information based on a list of house numbers.
    Args:
        houseNumbers (List[str]): A list of house numbers to filter the query.
        db (Session, optional): Database session dependency. Defaults to
            the session provided by `getSession`.
    Returns:
        List[Dict]: A list of parsed house details, including associated
        tax records, assignments, and user information.
    """

    houses = db.exec(
        select(House,TaxRecord,Assignment,User)
        .outerjoin(TaxRecord, TaxRecord.houseId == House.houseNumber)
        .outerjoin(Assignment, Assignment.houseId == House.houseNumber)
        .outerjoin(User, User.username == Assignment.username)
        .where(House.houseNumber.in_(houseNumbers))
    ).all()
    return parseHouseGETResponse(houses)


def parseHouseGETResponse(results: any):
    """
    Parses the results of a database query into a list of `HouseGETResponse` objects.
    Args:
        results (any): A collection of tuples where each tuple contains:
            - house: An object representing house details.
            - taxRecord: An object representing tax record details (optional).
            - assignment: An object representing collector assignment details (optional).
            - user: An object representing user details (optional).
    Returns:
        list: A list of `HouseGETResponse` objects, each containing:
            - assessmentNumber: The assessment number of the house.
            - houseNumber: The house number.
            - houseValue: The value of the house.
            - houseTax: The house tax amount.
            - waterTax: The water tax amount.
            - libraryTax: The library tax amount.
            - lightingTax: The lighting tax amount.
            - drianageTax: The drainage tax amount.
            - husbandOrFatherNameOfOwner: The name of the husband or father of the house owner.
            - ownerName: The name of the house owner.
            - taxRecords: A list containing a single `TaxRecordGETResponse` object if `taxRecord` is provided, otherwise `None`.
            - collectorAssignments: A list containing a single `AssignmentGETRequest` object if `assignment` is provided, otherwise `None`.
            - users: A list containing a single `UserGetResponse` object if `user` is provided, otherwise `None`.
    """

    houses = []
    for house, taxRecord, assignment, user in results:
        houses.append(HouseGETResponse(
            assessmentNumber=house.assessmentNumber,
            houseNumber=house.houseNumber,
            houseValue=house.houseValue,
            houseTax=house.houseTax,
            waterTax=house.waterTax,
            libraryTax=house.libraryTax,
            lightingTax=house.lightingTax,
            drianageTax=house.drianageTax,
            husbandOrFatherNameOfOwner=house.husbandOrFatherNameOfOwner,
            ownerName=house.ownerName,
            taxRecords= [TaxRecordGETResponse(**taxRecord.model_dump())] if taxRecord else None,
            collectorAssignments=[AssignmentGETRequest(**assignment.model_dump())] if assignment else None,
            users=[UserGetResponse(**user.model_dump())] if user else None
        ))
    return houses

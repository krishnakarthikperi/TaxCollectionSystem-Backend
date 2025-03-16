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
        db: Session = Depends(getSession)
):
    houseNumbers = [house.houseNumber for house in houses]
    db.add_all(houses)
    db.commit()
    houses = getHousesByHouseNumbers(houseNumbers=houseNumbers, db=db)
    return houses

def getHouses(
    db: Session = Depends(getSession)
):
    results = db.exec(
        select(House,TaxRecord,Assignment,User)
        .outerjoin(TaxRecord, TaxRecord.houseId == House.houseNumber)
        .outerjoin(Assignment, Assignment.houseId == House.houseNumber)
        .outerjoin(User, User.username == Assignment.username)
    ).all()
    return parseHouseGETResponse(results)

def getHousesByHouseNumbers(
    houseNumbers: List[str],
    db: Session = Depends(getSession)
):
    houses = db.exec(
        select(House,TaxRecord,Assignment,User)
        .outerjoin(TaxRecord, TaxRecord.houseId == House.houseNumber)
        .outerjoin(Assignment, Assignment.houseId == House.houseNumber)
        .outerjoin(User, User.username == Assignment.username)
        .where(House.houseNumber.in_(houseNumbers))
    ).all()
    return parseHouseGETResponse(houses)

def parseHouseGETResponse(results: any):
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
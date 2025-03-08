from fastapi import Depends
from sqlmodel import Session
from auth.auth import tokenManagement
from db import SessionDep, getSession
from objects.house import House, HousePOSTRequest, HouseGETRequest
from objects.taxrecord import TaxRecord

ADMIN_ROLE = "ADMIN"
STANDARD_ROLE = "STANDARD_USER"

def createHouse(
        house: HousePOSTRequest,
        db: Session = Depends(getSession)
):
    db.add(house)
    db.commit()
    db.refresh(house)
    return house

def getHouses(
    db: Session = Depends(getSession)
):
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber)
    return houses

def getHousesByHouseNumber(
    house: HouseGETRequest,
    db: Session = Depends(getSession)
):
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber, House.houseNumber == house.houseNumber)
    return houses

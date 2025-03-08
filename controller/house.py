from auth.auth import tokenManagement
from db import SessionDep
from objects.house import House, HousePOSTRequest, HouseGETRequest
from objects.taxrecord import TaxRecord

ADMIN_ROLE = "ADMIN"
STANDARD_ROLE = "STANDARD_USER"

def createHouse(
        house: HousePOSTRequest,
        db: SessionDep
):
    db.add(house)
    db.commit()
    db.refresh(house)
    return house

def getHouses(
    db: SessionDep
):
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber)
    return houses

def getHousesByHouseNumber(
    house: HouseGETRequest,
    db: SessionDep
):
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber, House.houseNumber == house.houseNumber)
    return houses

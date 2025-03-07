from auth.auth import tokenManagement
from db import SessionDep
from objects.house import House, HousePOST, HouseGET
from objects.taxrecord import TaxRecord

ADMIN_ROLE = "ADMIN"
STANDARD_ROLE = "STANDARD_USER"

def createHouse(
        house: HousePOST,
        db: SessionDep
):
    house = House(**house.dict())
    db.add(house)
    db.commit()
    db.refresh(house)
    return house

def getHouses(
    token: str,
    db: SessionDep
):
    payload = tokenManagement.decodeAuthToken(token=token)
    context = payload.get('context')
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber)
    return houses

def getHousesByHouseNumber(
    house: HouseGET,
    db: SessionDep
):
    houses = db.query(House,TaxRecord).where(TaxRecord.houseId == House.HouseNumber, House.houseNumber == house.houseNumber)
    # if context.role == ADMIN_ROLE:
    # elif context.role == STANDARD_ROLE:
    #     houses = db.query(House,TaxRecord).join(Assignment).where(TaxRecord.houseId == House.HouseNumber, Assignment.username == context.user.key)
    return houses

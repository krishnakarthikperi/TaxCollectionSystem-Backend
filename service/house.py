from typing import List
from fastapi import APIRouter
import controller.house as controller
from objects.house import House, HouseGETRequest, HousePOSTRequest
from db import SessionDep

router = APIRouter()

@router.post("/house", response_model=HousePOSTRequest)
def createHouse(
        house: HousePOSTRequest,
        db: SessionDep
):
    house = House(**house.model_dump())
    return controller.createHouse(house=house,db=db)

@router.get("/households", response_model=List[HouseGETRequest])
def getHouses(
    db: SessionDep
):
    return controller.getHouses(db=db)    

@router.get("/households/{household_id}", response_model=HouseGETRequest)
def getHousesByHouseNumber(
    house: HouseGETRequest,
    db: SessionDep
):
    return controller.getHousesByHouseNumber(house=house,db=db)
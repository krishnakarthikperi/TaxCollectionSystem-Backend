from typing import List
from fastapi import APIRouter, Depends
from auth.auth import getCurrentUser
import controller.house as controller
from objects.house import House, HouseGETRequest, HousePOSTRequest

router = APIRouter()

@router.post("/house", response_model=HousePOSTRequest, dependencies=[Depends(getCurrentUser)])
def createHouse(
        house: HousePOSTRequest
):
    house = House(**house.model_dump())
    return controller.createHouse(house=house)

@router.get("/households", response_model=List[HouseGETRequest], dependencies=[Depends(getCurrentUser)])
def getHouses():
    return controller.getHouses()

@router.get("/households/{household_id}", response_model=HouseGETRequest, dependencies=[Depends(getCurrentUser)])
def getHousesByHouseNumber(
    house: HouseGETRequest
):
    return controller.getHousesByHouseNumber(house=house)
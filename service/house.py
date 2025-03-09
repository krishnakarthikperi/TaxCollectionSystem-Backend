from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.house as controller
from db import getSession
from objects.house import House, HouseGETRequest, HousePOSTRequest

router = APIRouter()

@router.post("/house", response_model=HousePOSTRequest, dependencies=[Depends(getCurrentUser)])
def createHouse(
        house: HousePOSTRequest,
        db: Session = Depends(getSession)
):
    house = House(**house.model_dump())
    return controller.createHouse(house=house, db=db)

@router.get("/households", response_model=List[HouseGETRequest], dependencies=[Depends(getCurrentUser)])
def getHouses(
    db: Session = Depends(getSession)
):
    return controller.getHouses(db=db)

@router.get("/households/{household_id}", response_model=HouseGETRequest, dependencies=[Depends(getCurrentUser)])
def getHousesByHouseNumber(
    house: HouseGETRequest,
    db: Session = Depends(getSession)
):
    return controller.getHousesByHouseNumber(house=house, db=db)
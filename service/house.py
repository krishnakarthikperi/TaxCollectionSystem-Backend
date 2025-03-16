from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.house as controller
from db import getSession
from objects.house import House, HouseGETRequest, HouseGETResponse, HousePOSTRequest

router = APIRouter()

@router.post("/house", response_model=List[HousePOSTRequest], dependencies=[Depends(getCurrentUser)])
def createHouses(
        houses: List[HousePOSTRequest],
        db: Session = Depends(getSession)
):
    newHouses = [House(**house.model_dump()) for house in houses]
    return controller.createHouses(houses=newHouses, db=db)

@router.get("/households", response_model=List[HouseGETResponse], dependencies=[Depends(getCurrentUser)])
def getHouses(
    db: Session = Depends(getSession)
):
    return controller.getHouses(db=db)

@router.get("/households/{household_id}", response_model=List[HouseGETResponse], dependencies=[Depends(getCurrentUser)])
def getHousesByHouseNumber(
    household_id: str,
    db: Session = Depends(getSession)
):
    houses = [HouseGETRequest(houseNumber=household_id)]
    houseNumbers = [house.houseNumber for house in houses]
    return controller.getHousesByHouseNumbers(houseNumbers=houseNumbers, db=db)
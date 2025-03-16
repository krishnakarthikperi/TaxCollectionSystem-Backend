from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.assignment as controller
import controller.user as UserController
import controller.house as HouseController
from db import getSession
from objects.assignment import Assignment, AssignmentGETRequest, AssignmentPOSTRequest
from objects.house import HouseGETRequest
import controller.house as HouseController
import service.constants as constants 

router = APIRouter()

@router.post("/assign-collector", response_model=AssignmentPOSTRequest, dependencies=[Depends(getCurrentUser)])
def assignVolunteer(
        assignment: AssignmentPOSTRequest,
        db: Session = Depends(getSession)
):
    user = UserController.getUserByUsername(username=assignment.username,db=db)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = constants.INVALID_VOLUNTEER_DETAILS
        )
    house = HouseController.getHousesByHouseNumber(HouseGETRequest(houseNumber=assignment.houseId))
    if not house:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = constants.INVALID_HOUSE_NUMBER
        )
    new_assignment = Assignment(**assignment.model_dump())
    return controller.assignVolunteer(assignment=new_assignment, db=db)
    

@router.get("/assignments/{collector_id}", response_model=List[AssignmentGETRequest])
def getAssignmentsByUser(
        user=Depends(getCurrentUser),
        db: Session = Depends(getSession)
):
    return controller.getAssignmentsByUser(username=user.username,db=db)
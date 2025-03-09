from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from auth.auth import getCurrentUser
import controller.assignment as controller
import controller.user as UserController
import controller.house as HouseController
from db import getSession
from objects.assignment import Assignment, assignmentGETRequest, assignmentPOSTRequest
from objects.house import HouseGETRequest
import controller.house as HouseController 

router = APIRouter()

@router.post("/assign-collector", response_model=assignmentPOSTRequest, dependencies=[Depends(getCurrentUser)])
def assignVolunteer(
        assignment: assignmentPOSTRequest,
        db: Session = Depends(getSession)
):
    user = UserController.getUserByUsername(username=assignment.username,db=db)
    if not user:
        raise HTTPException(
            status_code = 400,
            detail="Invalid volunteer details"
        )
    house = HouseController.getHousesByHouseNumber(HouseGETRequest(houseNumber=assignment.houseId))
    if not house:
        raise HTTPException(
            status_code = 400,
            detail="Invalid house number"
        )
    new_assignment = Assignment(**assignment.model_dump())
    return controller.assignVolunteer(assignment=new_assignment, db=db)
    

@router.get("/assignments/{collector_id}", response_model=List[assignmentGETRequest])
def getAssignmentsByUser(
        user=Depends(getCurrentUser),
        db: Session = Depends(getSession)
):
    return controller.getAssignmentsByUser(username=user.username,db=db)
from typing import List
from fastapi import APIRouter, HTTPException
import controller.assignment as controller
import controller.user as UserController
import controller.house as HouseController
from db import SessionDep
from objects.assignment import Assignment, assignmentGETRequest, assignmentPOSTRequest
from objects.house import House

router = APIRouter()

@router.post("/assign-collector", response_model=assignmentPOSTRequest)
def assignVolunteer(
        assignment: assignmentPOSTRequest,
        db: SessionDep,
):
    user = UserController.getUserByUsername(username=assignment.username,db=db)
    if not user:
        raise HTTPException(
            status_code = 400,
            detail="Invalid volunteer details"
        )
    house = db.get(House,assignment.houseId)
    if not house:
        raise HTTPException(
            status_code = 400,
            detail="Invalid house number"
        )
    new_assignment = Assignment(**assignment.model_dump())
    return controller.assignVolunteer(assignment=new_assignment,db=SessionDep)
    

@router.get("/assignments/{collector_id}", response_model=List[assignmentGETRequest])
def getAssignmentsByUser(
        username: str,
        db: SessionDep
):
    return controller.getAssignmentsByUser(username=username, db=db)
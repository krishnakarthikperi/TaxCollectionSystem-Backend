from db import SessionDep
from fastapi import HTTPException
from objects.assignment import Assignment, assignmentGET, assignmentPOST
from objects.user import User
from objects.house import House

def assignVolunteer(
        assignment: assignmentPOST,
        db: SessionDep,
):
    volunteer = db.get(User, assignment.username)
    if not volunteer:
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
    
    new_assignment = Assignment(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

def getAssignmentsByUser(
        username: str,
        db: SessionDep
):
    assignments = db.exec(select(Assignment, House).where(Assignment.username == username, Assignment.houseId == House.houseNumber)).all()
    return assignments
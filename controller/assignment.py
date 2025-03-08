from sqlmodel import select
from db import SessionDep
from fastapi import HTTPException
from objects.assignment import Assignment, assignmentGETRequest, assignmentPOSTRequest
from objects.user import User
from objects.house import House

def assignVolunteer(
        assignment: assignmentPOSTRequest,
        db: SessionDep,
):  
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def getAssignmentsByUser(
        username: str,
        db: SessionDep
):
    assignments = db.exec(select(Assignment, House).where(Assignment.username == username, Assignment.houseId == House.houseNumber)).all()
    return assignments
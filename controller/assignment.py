from sqlmodel import Session, select
from db import getSession
from fastapi import Depends
from objects.assignment import Assignment, AssignmentPOSTRequest
from objects.house import House

def assignVolunteer(
        assignment: AssignmentPOSTRequest,
        db: Session = Depends(getSession)
):  
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def getAssignmentsByUser(
        username: str,
        db: Session = Depends(getSession)
):
    assignments = db.exec(select(Assignment, House).where(Assignment.username == username, Assignment.houseId == House.houseNumber)).all()
    return assignments

def getAssignmentsByUsernameAndHouseNumber(
        username: str,
        houseNumber:str,
        db: Session = Depends(getSession)
):
    assignment = db.exec(select(Assignment, House).where(Assignment.username == username, Assignment.houseId == houseNumber)).first()
    return assignment
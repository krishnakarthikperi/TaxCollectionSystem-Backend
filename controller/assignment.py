from sqlmodel import Session, select
from db import SessionDep, getSession
from fastapi import Depends, HTTPException
from objects.assignment import Assignment, assignmentGETRequest, assignmentPOSTRequest
from objects.user import User
from objects.house import House

def assignVolunteer(
        assignment: assignmentPOSTRequest,
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
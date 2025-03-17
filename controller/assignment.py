from typing import List
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

def getAssignmentsByUsernameAndHouseNumbers(
        username: str,
        houseNumbers:List[str],
        db: Session = Depends(getSession)
):
    assignments = db.exec(
        select(Assignment)
        .join(House, Assignment.houseId == House.houseNumber)
        .where(Assignment.username == username)
        .where(Assignment.houseId.in_(houseNumbers))
    ).all()
    return assignments
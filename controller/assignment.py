"""
This module provides functions for managing volunteer assignments in a tax collection system.
Functions:
    assignVolunteer(assignment: AssignmentPOSTRequest, db: Session) -> Assignment:
        Assigns a volunteer to a task by adding the assignment to the database.
    getAssignmentsByUser(username: str, db: Session) -> List[Tuple[Assignment, House]]:
        Retrieves all assignments for a specific user, including associated house details.
    getAssignmentsByUsernameAndHouseNumbers(username: str, houseNumbers: List[str], db: Session) -> List[Assignment]:
        Retrieves assignments for a specific user filtered by a list of house numbers.
"""

from typing import List
from sqlmodel import Session, select
from db import getSession
from fastapi import Depends
from objects.assignment import Assignment, AssignmentPOSTRequest
from objects.house import House


def assignVolunteer(
    assignment: AssignmentPOSTRequest,
    db: Session = Depends(getSession),
):
    """
    Assigns a volunteer by adding the provided assignment to the database.
    Args:
        assignment (AssignmentPOSTRequest): The assignment data to be added to the database.
        db (Session, optional): The database session dependency. Defaults to a session provided by `getSession`.
    Returns:
        AssignmentPOSTRequest: The newly added assignment after being committed and refreshed in the database.
    """
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def getAssignmentsByUser(
    username: str,
    db: Session = Depends(getSession),
):
    """
    Retrieve assignments associated with a specific user.
    Args:
        username (str): The username of the user whose assignments are to be retrieved.
        db (Session, optional): The database session dependency. Defaults to a session provided by `getSession`.
    Returns:
        List[Tuple[Assignment, House]]: A list of tuples containing Assignment and House objects
        where the assignment is linked to the specified user and the house ID matches the house number.
    """

    assignments = db.exec(
        select(Assignment, House).where(
            Assignment.username == username, Assignment.houseId == House.houseNumber
        )
    ).all()
    return assignments


def getAssignmentsByUsernameAndHouseNumbers(
    username: str,
    houseNumbers: List[str],
    db: Session = Depends(getSession),
):
    """
    Retrieve assignments for a specific user and a list of house numbers.
    Args:
    username (str): The username of the user whose assignments are to be retrieved.
    houseNumbers (List[str]): A list of house numbers to filter the assignments.
    db (Session, optional): The database session dependency. Defaults to the result of `getSession`.
    Returns:
    List[Assignment]: A list of Assignment objects that match the specified username and house numbers.
    """

    assignments = db.exec(
        select(Assignment)
        .join(House, Assignment.houseId == House.houseNumber)
        .where(Assignment.username == username)
        .where(Assignment.houseId.in_(houseNumbers))
    ).all()
    return assignments

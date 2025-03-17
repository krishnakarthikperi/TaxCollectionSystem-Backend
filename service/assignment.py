"""
This module defines API endpoints for managing assignments in the Tax Collection service.
Endpoints:
- POST /assign-collector: Assigns a volunteer (collector) to a house based on the provided assignment details.
- GET /assignments/{collector_id}: Retrieves a list of assignments for a specific user.
Dependencies:
- FastAPI's APIRouter is used to define the routes.
- SQLModel's Session is used for database interactions.
- Authentication dependencies ensure that only authorized users can access certain endpoints.
Functions:
- assignVolunteer: Assigns a volunteer to a house. Validates the user and house details before creating the assignment.
- getAssignmentsByUser: Retrieves all assignments associated with the currently authenticated user.
Imports:
- FastAPI modules for routing, dependency injection, and HTTP exceptions.
- SQLModel for database session management.
- Custom controllers and objects for handling business logic and data models.
- Constants for error messages and other reusable values.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from auth.auth import getCurrentAdmin, getCurrentUser
import controller.assignment as controller
import controller.user as UserController
import controller.house as HouseController
from db import getSession
from objects.assignment import Assignment, AssignmentGETRequest, AssignmentPOSTRequest
from objects.house import HouseGETRequest
import controller.house as HouseController
import service.constants as constants 

router = APIRouter()


@router.post(
    "/assign-collector",
    response_model=AssignmentPOSTRequest,
    dependencies=[Depends(getCurrentAdmin)],
)
def assignVolunteer(
    assignment: AssignmentPOSTRequest,
    db: Session = Depends(getSession),
):
    """
    Assigns a volunteer to a specific house based on the provided assignment details.
    Args:
        assignment (AssignmentPOSTRequest): The assignment details containing the username of the volunteer
            and the house ID to be assigned.
        db (Session, optional): The database session dependency.
    Raises:
        HTTPException: If the user specified in the assignment does not exist.
        HTTPException: If the house specified in the assignment does not exist.
    Returns:
        Any: The result of the volunteer assignment operation.
    """

    user = UserController.getUserByUsername(
        username=assignment.username,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.INVALID_VOLUNTEER_DETAILS,
        )
    houses = HouseController.getHousesByHouseNumbers(
        houseNumbers=[assignment.houseId],
        db=db,
    )
    if not houses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.INVALID_HOUSE_NUMBER,
        )
    new_assignment = Assignment(**assignment.model_dump())
    return controller.assignVolunteer(
        assignment=new_assignment,
        db=db,
    )


@router.get(
    "/assignments/{collector_id}",
    response_model=List[AssignmentGETRequest],
)
def getAssignmentsByUser(
    user=Depends(getCurrentUser),
    db: Session = Depends(getSession),
):
    """
    Retrieve assignments for the currently authenticated user.
    Args:
        user (User): The currently authenticated user, automatically injected by Depends(getCurrentUser).
        db (Session): The database session, automatically injected by Depends(getSession).
    Returns:
        List[Assignment]: A list of assignments associated with the authenticated user.
    """

    return controller.getAssignmentsByUser(
        username=user.username,
        db=db,
    )

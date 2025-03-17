"""
This module defines the API routes and handlers for user-related operations.
Routes:
    - POST /register: Registers a new user. Requires admin authentication.
Dependencies:
    - getCurrentAdmin: Ensures the request is made by an authenticated admin.
    - getSession: Provides a database session for the request.
Modules:
    - auth.auth: Contains authentication-related utilities.
    - db: Provides database session management.
    - objects.user: Defines request and response models for user operations.
    - controller.user: Contains the business logic for user-related operations.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentAdmin
from db import getSession
from objects.user import UserPOSTRequest, UserPOSTResponse
import controller.user as UserController

router = APIRouter()


@router.post(
    "/register",
    response_model=UserPOSTResponse,
    dependencies=[Depends(getCurrentAdmin)],
)
def register(
    userDetails: UserPOSTRequest,
    db: Session = Depends(getSession),
):
    """
    Registers a new user in the system.

    Args:
        userDetails (UserPOSTRequest): The details of the user to be registered.
        db (Session, optional): The database session dependency. Defaults to the result of `Depends(getSession)`.

    Returns:
        Any: The result of the user registration process, as handled by the UserController.
    """
    return UserController.register(
        userDetails=userDetails,
        db=db,
    )

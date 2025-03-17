"""
This module provides user-related operations for the Tax Collection system.
Functions:
    getUserByUsername(username: str, db: Session):
        Retrieves a user by their username from the database.
    register(userDetails: UserPOSTRequest, db: Session):
        Registers a new user in the database. Raises an HTTPException if a user
        with the same username already exists.
Dependencies:
    - FastAPI's Depends for dependency injection.
    - SQLModel's Session for database interactions.
    - Custom modules for authentication, database session, and constants.
"""

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from auth.authcheck import hashPassword
from db import SessionDep, getSession
from objects.user import User, UserPOSTRequest
from service.constants import USERNAME_ALREADY_REGISTERED


def getUserByUsername(
    username: str,
    db: Session = Depends(getSession),
):
    """
    Retrieve a user by their username from the database.
    Args:
        username (str): The username of the user to retrieve.
        db (Session, optional): The database session dependency. Defaults to a session provided by `getSession`.
    Returns:
        User: The user object corresponding to the given username, or None if no user is found.
    """
    return db.get(User, username)


def register(
    userDetails: UserPOSTRequest,
    db: Session = Depends(getSession),
):
    """
    Registers a new user in the system.
    Args:
        userDetails (UserPOSTRequest): The details of the user to be registered.
        db (Session, optional): The database session dependency.
    Raises:
        HTTPException: If a user with the same username already exists.
    Returns:
        User: The newly registered user object.
    """

    # Check if a user with the same username already exists
    existing_user = db.get(User, userDetails.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_ALREADY_REGISTERED)

    user = User(**userDetails.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

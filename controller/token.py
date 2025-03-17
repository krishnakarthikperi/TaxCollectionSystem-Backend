"""
This module provides functionality for managing tokens in the application.
Functions:
        addToken(token: str, db: Session):
                Adds a new token to the database, commits the transaction, and refreshes the token instance.
Dependencies:
        - FastAPI's Depends for dependency injection.
        - SQLModel's Session for database interaction.
        - getSession from the db module to retrieve a database session.
"""

from fastapi import Depends
from sqlmodel import Session
from db import getSession


def addToken(
    token: str,
    db: Session = Depends(getSession),
):
    """
    Adds a new token to the database.
    Args:
            token (str): The token to be added to the database.
            db (Session, optional): The database session dependency. Defaults to Depends(getSession).
    Returns:
            str: The added token after being committed and refreshed in the database.
    """
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

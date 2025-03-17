"""
This module defines the authentication-related API endpoints for the Tax Collection service.
Routes:
    - POST /token: Authenticates a user and returns an access token.
    - POST /token/refresh: Refreshes an expired access token using a refresh token.
    - POST /logout: Logs out the currently authenticated user by invalidating their token.
Functions:
    - login(formData: OAuth2PasswordRequestForm, db: Session): Handles user login and token generation.
    - refreshToken(refreshToken: RefreshTokenPOSTRequest, db: Session): Handles token refresh requests.
    - logout(token: str, db: Session): Logs out the user by invalidating the provided token.
Dependencies:
    - Depends(getSession): Provides a database session for each request.
    - Depends(auth.getCurrentUser): Ensures the user is authenticated for the logout endpoint.
    - Depends(oauth2Scheme): Extracts the token from the request for logout.
Models:
    - UserAuthSuccess: Response model for successful authentication.
    - RefreshTokenPOSTRequest: Request model for token refresh.
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from auth import auth
from db import getSession
from objects.user import UserAuthSuccess
from auth.auth import oauth2Scheme
from objects.tokens import RefreshTokenPOSTRequest


router = APIRouter()
@router.post(
    "/token",
    response_model=UserAuthSuccess,
)
def login(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(getSession)
):
    """
    Handles user login by validating credentials and returning authentication details.
    Args:
        formData (OAuth2PasswordRequestForm): The form data containing user credentials.
        db (Session): The database session dependency.
    Returns:
        Any: The result of the authentication process, typically including tokens or user details.
    """

    return auth.login(
        formData=formData,
        db=db,
    )

@router.post("/token/refresh")
def refreshToken(
    refreshToken: RefreshTokenPOSTRequest,
    db: Session = Depends(getSession)
):
    """
    Refreshes the authentication token using the provided refresh token.

    Args:
        refreshToken (RefreshTokenPOSTRequest): The request object containing the refresh token.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.

    Returns:
        Any: The result of the token refresh operation, as handled by the `auth.refreshToken` method.
    """
    return auth.refreshToken(
        refreshToken=refreshToken,
        db=db,
    )


@router.post(
    "/logout",
    dependencies=[Depends(auth.getCurrentUser)],
)
def logout(
    token: str = Depends(oauth2Scheme), 
    db: Session = Depends(getSession)
):
    """
    Logs out a user by invalidating their authentication token.

    Args:
        token (str): The authentication token provided by the user.
            Retrieved using the OAuth2 scheme dependency.
        db (Session): The database session dependency used to interact
            with the database.

    Returns:
        Any: The result of the logout operation, as defined by the
            `auth.logout` function.
    """
    return auth.logout(
        token=token,
        db=db,
    )

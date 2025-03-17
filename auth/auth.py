"""
This module provides authentication and authorization functionalities for a FastAPI application.
It includes token management, user authentication, and role-based access control.
Classes:
- TokenManagement:
    A class for managing JSON Web Tokens (JWTs), including encoding, decoding, and validation.
Functions:
----------
- authenticateUser(username: str, password: str, db: Session):
- getCurrentUser(token: str, db: Session):
    Retrieves the current authenticated user based on the provided token.
- login(formData: OAuth2PasswordRequestForm, db: Session):
- refreshToken(refreshToken: RefreshTokenPOSTRequest, db: Session):
    Handles the refresh token process by validating the provided refresh token and generating a new access token.
- logout(token: str, db: Session):
- getCurrentAdmin(user: User):
Dependencies:
-------------
- OAuth2PasswordBearer: Used for extracting and validating Bearer tokens from requests.
- Session: SQLAlchemy database session dependency for database operations.
Constants:
----------
- ACCESS_TOKEN_EXPIRE_MINUTES: The expiration time for access tokens in minutes.
- REFRESH_TOKEN_EXPIRE_DAYS: The expiration time for refresh tokens in days.
- ACCESS_SECRET_KEY: The secret key for signing access tokens.
- REFRESH_SECRET_KEY: The secret key for signing refresh tokens.
- ALGORITHM: The algorithm used for encoding and decoding JWTs.
Exceptions:
-----------
- HTTPException: Raised for various authentication and authorization errors, such as invalid credentials,
  insufficient permissions, or expired tokens.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionDep, getSession
from objects.tokens import RefreshTokenPOSTRequest, RevokedToken
from objects.user import User,UserAuthSuccess
from service.constants import COULD_NOT_VALIDATE_CREDENTIALS, INSUFFICIENT_PERMISSIONS, INVALID_CREDENTIALS, INVALID_REFRESH_TOKEN, INVALID_TOKEN, LOGGED_OUT_SUCCESSFULLY, TOKEN_EXPIRED, USER_NOT_FOUND, USER_ROLE_ADMIN
from .authcheck import verifyPassword, hashPassword
from .authconstants import ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from .authconstants import ALGORITHM
from .authconstants import REFRESH_SECRET_KEY
from .authconstants import REFRESH_TOKEN_EXPIRE_DAYS
from .authconstants import ACCESS_SECRET_KEY
import uuid
import controller.user as UserController
import controller.token as TokenController

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenManagement:
    """
    TokenManagement Class
    This class provides methods for encoding, decoding, and validating JSON Web Tokens (JWTs) for authentication and refresh purposes.
    Methods:
    --------
        __encodeToken(payload: dict, SECRET_KEY: str, expiresDelta: timedelta = None) -> str:
        encodeAuthToken(payload: dict, expiresDelta: timedelta = None) -> str:
        encodeRefreshToken(payload: dict, expiresDelta: timedelta = None) -> str:
        __decodeToken(token: str, SECRET_KEY: str) -> dict or None:
        decodeAuthToken(token: str) -> dict or None:
        decodeRefreshToken(token: str) -> dict or None:
        tokenValidation(token: str, tokenType: str = ACCESS_TOKEN_TYPE) -> dict or None:
    """

    def __encodeToken(
            self,
            payload: dict, 
            SECRET_KEY: str, 
            expiresDelta: timedelta = None
        ):
        """
        Encodes a JWT token with the given payload, secret key, and optional expiration time.
        Parameters:
            - payload (dict): The data to include in the token.
            - SECRET_KEY (str): The secret key used to sign the token.
            - expiresDelta (timedelta, optional): The time duration after which the token will expire. Defaults to `ACCESS_TOKEN_EXPIRE_MINUTES`.
        Returns:
            - str: The encoded JWT token.
        """
        toEncode = payload.copy()
        expire = datetime.now(timezone.utc)+(expiresDelta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        jti = str(uuid.uuid4())
        toEncode.update(
            {
                "exp":expire,
                "jti":jti
            }
        )
        return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)        

    def encodeAuthToken(self,payload:dict, expiresDelta: timedelta = None):
        """
        Encodes an authentication token using the access secret key.
        Parameters:
            - payload (dict): The data to include in the token.
            - expiresDelta (timedelta, optional): The time duration after which the token will expire.
        Returns:
            - str: The encoded authentication token.
        """
        return self.__encodeToken(payload=payload,SECRET_KEY = ACCESS_SECRET_KEY, expiresDelta = expiresDelta)

    def encodeRefreshToken(self,payload:dict, expiresDelta: timedelta = None):
        """
        Encodes a refresh token using the refresh secret key.
        Parameters:
            - payload (dict): The data to include in the token.
            - expiresDelta (timedelta, optional): The time duration after which the token will expire.
        Returns:
            - str: The encoded refresh token.
        """
        return self.__encodeToken(payload=payload,SECRET_KEY = REFRESH_SECRET_KEY, expiresDelta = expiresDelta)

    def __decodeToken(self, token: str, SECRET_KEY: str):
        """
        Decodes a JWT token using the given secret key.
        Parameters:
            - token (str): The JWT token to decode.
            - SECRET_KEY (str): The secret key used to decode the token.
        Returns:
            - dict: The decoded payload if the token is valid.
            - None: If the token is invalid or decoding fails.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def decodeAuthToken(self, token: str):
        """
        Decodes an authentication token using the access secret key.
        Parameters:
            - token (str): The authentication token to decode.
        Returns:
            - dict: The decoded payload if the token is valid.
            - None: If the token is invalid or decoding fails.
        """
        return self.__decodeToken(token=token, SECRET_KEY=ACCESS_SECRET_KEY)

    def decodeRefreshToken(self, token: str):
        """
        Decodes a refresh token using the refresh secret key.
        Parameters:
            - token (str): The refresh token to decode.
        Returns:
            - dict: The decoded payload if the token is valid.
            - None: If the token is invalid or decoding fails.
        """
        return self.__decodeToken(token=token, SECRET_KEY=REFRESH_SECRET_KEY)

    def tokenValidation(self, token: str, tokenType: str = ACCESS_TOKEN_TYPE):
        credentialsException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= COULD_NOT_VALIDATE_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"}
        )
        """
        Validates a token based on its type (access or refresh) and checks for expiration.
        Parameters:
            - token (str): The token to validate.
            - tokenType (str, optional): The type of token to validate. Defaults to `ACCESS_TOKEN_TYPE`.
        Returns:
            - dict: The decoded payload if the token is valid.
            - None: If the token is invalid or the type is unsupported.
        Raises:
            - HTTPException: If the token is invalid, expired, or the credentials cannot be validated.
"""
        try:
            if tokenType == ACCESS_TOKEN_TYPE:
                payload =  self.decodeAuthToken(token=token)
            elif tokenType == REFRESH_TOKEN_TYPE:
                payload =  self.decodeRefreshToken(token=token)
            else:
                return None

            if payload is None:
                raise credentialsException
            username: str = payload.get("sub")
            exp: int = payload.get("exp")
            # Check if token has expired
            if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail=TOKEN_EXPIRED
                )
            if username is None:
                raise credentialsException
            return payload
        except JWTError:
            raise credentialsException


def authenticateUser(
    username: str,
    password: str,
    db: Session = Depends(getSession),
):
    """
    Authenticates a user by verifying their username and password.
    Args:
        username (str): The username of the user attempting to authenticate.
        password (str): The password provided by the user for authentication.
        db (Session, optional): The database session dependency. Defaults to the session provided by `getSession`.
    Returns:
        User: The authenticated user object if the username and password are valid.
        None: If authentication fails (invalid username or password).
    """
    user = UserController.getUserByUsername(
        username=username,
        db=db,
    )
    if user and verifyPassword(
        password,
        user.password,
    ):
        return user
    return None


def getCurrentUser(
        token: str = Depends(oauth2Scheme),
        db: Session = Depends(getSession)
    ):
    """
    Retrieve the current authenticated user based on the provided token.
    Args:
        token (str): The Bearer token extracted from the request's Authorization header.
                        This is validated using the OAuth2 scheme.
        db (Session): The database session dependency used to query the user information.
    Returns:
        User: The user object corresponding to the token's subject (username).
    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist in the database.
    """

    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=COULD_NOT_VALIDATE_CREDENTIALS,
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )
    payload = TokenManagement().tokenValidation(
        token=token,
        tokenType=ACCESS_TOKEN_TYPE,
    )
    user = UserController.getUserByUsername(
        username=payload.get("sub"),
        db=db,
    )
    if user is None:
        raise credentialsException # Change the exception
    return user

def login(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(getSession)
    ):
    """
    Handles user login by authenticating credentials and generating access and refresh tokens.
    Args:
        formData (Annotated[OAuth2PasswordRequestForm, Depends]): The form data containing the username and password.
        db (Session, optional): The database session dependency. Defaults to Depends(getSession).
    Returns:
        UserAuthSuccess: An object containing authentication details such as access token, refresh token,
                            username, name, phone, and user roles.
    Raises:
        HTTPException: If authentication fails, raises a 401 Unauthorized error with an appropriate message.
    """

    user = authenticateUser(
        username=formData.username,
        password=formData.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokenData = {
        "sub": user.username,
        "context": {
            "user": {"key": user.username, "phone": user.phone},
            "roles": user.userRole,
        },
    }
    accessToken = TokenManagement().encodeAuthToken(
        payload=tokenData,
        expiresDelta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refreshToken = TokenManagement().encodeRefreshToken(
        payload={"sub": user.username},
        expiresDelta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    authDetails = UserAuthSuccess(
        username=user.username,
        name=user.name,
        access_token=accessToken,
        phone=user.phone,
        refresh_token=refreshToken,
        userRole=user.userRole,
    )
    return authDetails


def refreshToken(
    refreshToken: RefreshTokenPOSTRequest,
    db: Session = Depends(getSession),
):
    """
    Handles the refresh token process by validating the provided refresh token,
    retrieving the associated user, and generating a new access token.
    Args:
        refreshToken (RefreshTokenPOSTRequest): The request object containing the refresh token.
        db (Session, optional): The database session dependency. Defaults to Depends(getSession).
    Raises:
        HTTPException: If the refresh token is invalid or expired.
        HTTPException: If the user associated with the token is not found.
    Returns:
        dict: A dictionary containing the new access token and its type.
    """

    payload = TokenManagement().tokenValidation(token=refreshToken.refresh_token, tokenType=REFRESH_TOKEN_TYPE)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_REFRESH_TOKEN,
        )
    username: str = payload.get("sub")
    user = UserController.getUserByUsername(
        username=username,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_FOUND,
        )
    newAccessToken = TokenManagement().encodeAuthToken(
        {
            "sub": user.username,
        },
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": newAccessToken, "token_type": "Bearer"}


def logout(
    token: str = Depends(oauth2Scheme),
    db: Session = Depends(SessionDep),
):
    """
    Logs out a user by revoking their access token.

    Args:
        token (str): The access token provided by the user, extracted using the OAuth2 scheme.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the provided token is invalid or unauthorized.

    Returns:
        dict: A dictionary containing a success message indicating the user has been logged out.
    """
    payload = TokenManagement().tokenValidation(token=token, tokenType=ACCESS_TOKEN_TYPE)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_TOKEN,
        )
    jti = payload.get("jti")
    revokedToken = RevokedToken(jti=jti)
    token = TokenController.addToken(
        token=revokedToken,
        db=db,
    )
    return {"message": LOGGED_OUT_SUCCESSFULLY}


def getCurrentAdmin(user=Depends(getCurrentUser)):
    """
    Validates if the current user has administrative privileges.
    This function checks the role of the authenticated user to ensure they
    have the necessary permissions to perform administrative actions. If the
    user does not have the required role, an HTTP 403 Forbidden exception is raised.
    Args:
        user (User): The authenticated user object, injected via dependency.
    Returns:
        User: The authenticated user object if they have administrative privileges.
    Raises:
        HTTPException: If the user does not have the 'ADMIN' role.
    """

    if USER_ROLE_ADMIN not in user.userRole.split(","):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=INSUFFICIENT_PERMISSIONS,
        )
    return user

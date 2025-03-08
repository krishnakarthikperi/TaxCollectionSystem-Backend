from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionDep
from objects.tokens import RevokedToken
from objects.user import User,UserAuthSuccess
from .authcheck import verifyPassword, hashPassword
from .authconstants import ACCESS_TOKEN_EXPIRE_MINUTES
from .authconstants import ALGORITHM
from .authconstants import REFRESH_SECRET_KEY
from .authconstants import REFRESH_TOKEN_EXPIRE_DAYS
from .authconstants import ACCESS_SECRET_KEY
import uuid
import controller.user as UserController
import controller.token as TokenController

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

class tokenManagement:
    def __encodeToken(
            payload: dict, 
            SECRET_KEY: str, 
            expiresDelta: timedelta = None
        ):
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

    def encodeAuthToken(self, payload:str, expiresDelta: timedelta = None):
        return self.__encodeToken(payload=payload,SECRET_KEY = ACCESS_SECRET_KEY, expiresDelta = expiresDelta)

    def encodeRefreshToken(self, payload:str, expiresDelta: timedelta = None):
        return self.__encodeToken(payload=payload,SECRET_KEY = REFRESH_SECRET_KEY, expiresDelta = expiresDelta)

    def __decodeToken(token: str, SECRET_KEY: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def decodeAuthToken(self, token: str):
        return self.__decodeToken(token=token, SECRET_KEY=ACCESS_SECRET_KEY)

    def decodeRefreshToken(self, token: str):
        return self.__decodeToken(token=token, SECRET_KEY=REFRESH_SECRET_KEY)


def authenticateUser(
        username: str, 
        password:str
    ):
    user =  UserController.getUserByUsername(username=username)
    if user and verifyPassword(password,user.password):
        return user
    return None

def getCurrentUser(
        token: str = Depends(oauth2Scheme) 
    ):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = tokenManagement.decodeAuthToken(token)
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        # Check if token has expired
        if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")
        if username is None:
            raise credentialsException
    except JWTError:
        raise credentialsException
    user =  UserController.getUserByUsername(username=username)
    if user is None:
        raise credentialsException
    return user

def login(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()]
        # password: str, 
        # username: str 
    ):
    user = authenticateUser(
        formData.username, 
        formData.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    tokenData = {
        "sub": user.username,
        "context":{
            "user":{
                "key":user.username,
                "phone":user.phone
            },
            "roles":user.userRole
        }        
    }
    accessToken = tokenManagement.encodeAuthToken(
        payload = tokenData, 
        timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refreshToken = tokenManagement.encodeRefreshToken(
        payload = {"sub": user.username}, 
        timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    authDetails = UserAuthSuccess(
        username=user.username,
        name=user.name,
        accessToken= accessToken,
        phone = user.phone,
        refreshToken = refreshToken
    )
    return authDetails

def refreshToken(
        refreshToken: str,
    ):
    payload = tokenManagement.decodeRefreshToken(token=refreshToken)
    if not payload:
        raise HTTPException(
            status_code=401, 
            detail="Invalid refresh token"
        )    
    username: str = payload.get("sub")
    user =  UserController.getUserByUsername(username=username)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="User not found"
        )
    newAccessToken = tokenManagement.encodeAuthToken(
        {
            "sub": user.username
        }, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": newAccessToken, "token_type": "bearer"}

def logout(
        token: str = Depends(oauth2Scheme), 
        db: Session = Depends(SessionDep)
    ):
    payload = tokenManagement.decodeAuthToken(token=token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    jti = payload.get("jti")
    revokedToken = RevokedToken(jti=jti)
    token = TokenController.addToken(token=revokedToken)   
    return {"message": "Logged out successfully"}

def getCurrentAdmin(user=Depends(getCurrentUser)):
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

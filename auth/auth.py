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
    def __encodeToken(
            self,
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

    def encodeAuthToken(self,payload:dict, expiresDelta: timedelta = None):
        return self.__encodeToken(payload=payload,SECRET_KEY = ACCESS_SECRET_KEY, expiresDelta = expiresDelta)

    def encodeRefreshToken(self,payload:dict, expiresDelta: timedelta = None):
        return self.__encodeToken(payload=payload,SECRET_KEY = REFRESH_SECRET_KEY, expiresDelta = expiresDelta)

    def __decodeToken(self, token: str, SECRET_KEY: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def decodeAuthToken(self, token: str):
        return self.__decodeToken(token=token, SECRET_KEY=ACCESS_SECRET_KEY)

    def decodeRefreshToken(self, token: str):
        return self.__decodeToken(token=token, SECRET_KEY=REFRESH_SECRET_KEY)
    
    def tokenValidation(self, token: str, tokenType: str = ACCESS_TOKEN_TYPE):
        credentialsException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= COULD_NOT_VALIDATE_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"}
        )
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
        password:str,
        db: Session = Depends(getSession)
    ):
    user =  UserController.getUserByUsername(username=username, db=db)
    if user and verifyPassword(password,user.password):
        return user
    return None

def getCurrentUser(
        token: str = Depends(oauth2Scheme),
        db: Session = Depends(getSession)
    ):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= COULD_NOT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = TokenManagement().tokenValidation(token=token, tokenType=ACCESS_TOKEN_TYPE)
    user =  UserController.getUserByUsername(username=payload.get("sub"),db=db)
    if user is None:
        raise credentialsException # Change the exception
    return user

def login(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(getSession)
    ):
    user = authenticateUser(
        username=formData.username, 
        password=formData.password,
        db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
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
    accessToken = TokenManagement().encodeAuthToken(
        payload = tokenData, 
        expiresDelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refreshToken = TokenManagement().encodeRefreshToken(
        payload = {"sub": user.username}, 
        expiresDelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    authDetails = UserAuthSuccess(
        username=user.username,
        name=user.name,
        access_token= accessToken,
        phone = user.phone,
        refresh_token = refreshToken,
        userRole = user.userRole
    )
    return authDetails

def refreshToken(
        refreshToken: RefreshTokenPOSTRequest,
        db: Session = Depends(getSession)
    ):
    payload = TokenManagement().tokenValidation(token=refreshToken.refresh_token, tokenType=REFRESH_TOKEN_TYPE)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = INVALID_REFRESH_TOKEN
        )
    username: str = payload.get("sub")
    user =  UserController.getUserByUsername(username=username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = USER_NOT_FOUND
        )
    newAccessToken = TokenManagement().encodeAuthToken(
        {
            "sub": user.username
        }, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": newAccessToken, "token_type": "Bearer"}

def logout(
        token: str = Depends(oauth2Scheme), 
        db: Session = Depends(SessionDep)
    ):
    payload = TokenManagement().tokenValidation(token=token, tokenType=ACCESS_TOKEN_TYPE)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=INVALID_TOKEN
        )
    jti = payload.get("jti")
    revokedToken = RevokedToken(jti=jti)
    token = TokenController.addToken(token=revokedToken,db=db)   
    return {"message": LOGGED_OUT_SUCCESSFULLY}

def getCurrentAdmin(user=Depends(getCurrentUser)):
    if USER_ROLE_ADMIN not in user.userRole.split(","):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=INSUFFICIENT_PERMISSIONS
        )
    return user

from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from auth import auth
from db import getSession
from objects.user import UserAuthSuccess
from auth.auth import oauth2Scheme

router = APIRouter()
@router.post("/token",response_model=UserAuthSuccess)
def login(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(getSession)
):
    return auth.login(
        formData=formData,
        db=db
    )

@router.post("/token/refresh", dependencies=[Depends(auth.getCurrentUser)])
def refreshToken(
    refreshToken: str,
    db: Session = Depends(getSession)
):
    return auth.refreshToken(
        refreshToken=refreshToken,
        db=db
    )

@router.post("/logout", dependencies=[Depends(auth.getCurrentUser)])
def logout(
    token: str = Depends(oauth2Scheme), 
    db: Session = Depends(getSession)
):
    return auth.logout(
        token=token,
        db=db
    )
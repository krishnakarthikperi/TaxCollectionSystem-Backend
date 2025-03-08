from typing import List
from fastapi import APIRouter, Depends
from auth import auth
from objects.user import UserAuthSuccess

router = APIRouter()
@router.post("/login",response_model=UserAuthSuccess)
def login(
    password: str, 
    username: str
):
    return auth.login(
        password=password, 
        username=username
    )

@router.post("/token/refresh", dependencies=[Depends(auth.getCurrentUser)])
def refreshToken(
    refreshToken: str
):
    return auth.refreshToken(
        refreshToken=refreshToken
    )

@router.post("/logout", dependencies=[Depends(auth.getCurrentUser)])
def logout(
    token: str
):
    return auth.logout(
        token=token
    )
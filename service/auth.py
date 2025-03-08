from fastapi import APIRouter
from auth import auth
from db import SessionDep
from objects.user import UserAuthSuccess

router = APIRouter()
@router.post("/login",response_model=UserAuthSuccess)
def login(
    password: str, 
    username: str, 
    db: SessionDep
):
    return auth.login(
        password=password, 
        username=username, 
        db=db
    )

@router.post("/token/refresh")
def refreshToken(
    refreshToken: str, 
    db: SessionDep
):
    return auth.refreshToken(
        refreshToken=refreshToken,
        db=db
    )

@router.post("/logout")
def logout(
    token: str, 
    db: SessionDep
):
    return auth.logout(
        token=token,
        db=db
    )
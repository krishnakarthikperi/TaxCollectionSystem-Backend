from typing import List
from fastapi import APIRouter
from auth import auth
from db import SessionDep
from objects.user import UserAuthSuccess, UserBase

router = APIRouter()

@router.post("/register",response_model=UserBase)
def register(
    name:str, 
    password: str, 
    phone: int,
    username: str, 
    db: SessionDep
):
    return auth.register(
        name=name, 
        password=password, 
        phone=phone,
        username=username, 
        db=db
    )

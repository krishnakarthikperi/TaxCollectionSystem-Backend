from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentAdmin
from db import getSession
from objects.user import UserBase, UserBase
import controller.user as UserController

router = APIRouter()

# @router.post("/register",response_model=UserBase, dependencies=[Depends(getCurrentAdmin)])
@router.post("/register",response_model=UserBase)
def register(
    name:str, 
    password: str, 
    phone: int,
    username: str,
    db: Session = Depends(getSession)
):
    return UserController.register(
        name=name, 
        password=password, 
        phone=phone,
        username=username,
        db = db 
    )

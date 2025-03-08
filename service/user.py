from typing import List
from fastapi import APIRouter, Depends
from auth.auth import getCurrentAdmin
from objects.user import UserBase, UserBase
import controller.user as UserController

router = APIRouter()

@router.post("/register",response_model=UserBase, dependencies=[Depends(getCurrentAdmin)])
def register(
    name:str, 
    password: str, 
    phone: int,
    username: str, 
):
    return UserController.register(
        name=name, 
        password=password, 
        phone=phone,
        username=username, 
    )

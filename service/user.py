from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from auth.auth import getCurrentAdmin
from db import getSession
from objects.user import UserPOSTRequest, UserPOSTResponse
import controller.user as UserController

router = APIRouter()

@router.post("/register",response_model=UserPOSTResponse, dependencies=[Depends(getCurrentAdmin)])
def register(
    userDetails: UserPOSTRequest,
    db: Session = Depends(getSession)
):
    return UserController.register(
        userDetails = userDetails,
        db = db 
    )

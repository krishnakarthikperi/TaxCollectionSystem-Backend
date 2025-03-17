from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from auth.authcheck import hashPassword
from db import SessionDep, getSession
from objects.user import User, UserPOSTRequest
from service.constants import USERNAME_ALREADY_REGISTERED

def getUserByUsername(
        username: str,
        db: Session = Depends(getSession)
):
    return db.get(User, username)

def register(
        userDetails: UserPOSTRequest,
        db: Session = Depends(getSession)
    ):
    # Check if a user with the same username already exists
    existing_user = db.get(User, userDetails.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_ALREADY_REGISTERED)
    
    user = User(**userDetails.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
from fastapi import Depends
from sqlmodel import Session
from auth.authcheck import hashPassword
from db import getSession
from objects.user import User

def getUserByUsername(
        username: str,
        db: Session = Depends(getSession)
):
    return db.get(User, username)

def register(
        name:str, 
        password: str, 
        phone: int,
        username: str, 
        db: Session = Depends(getSession)
    ):
    user = User(
        name=name, 
        password=hashPassword(password),
        phone=phone,
        username=username, 
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
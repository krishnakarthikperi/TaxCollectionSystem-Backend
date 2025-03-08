from fastapi import Depends
from sqlmodel import Session
from db import getSession

def addToken(
        token: str,
        db: Session = Depends(getSession)
):
    db.add(token)
    db.commit()
    db.refresh(token)
    return token
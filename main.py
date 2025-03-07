from typing import Union
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from db import SessionDep
from auth import auth
from objects.user import User,UserBase, UserAuthSuccess
import data

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.post("/register",response_model=UserBase)
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

@app.post("/token",response_model=UserAuthSuccess)
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

@app.post("/token/refresh")
def refreshToken(
    refreshToken: str, 
    db: SessionDep
):
    return auth.refreshToken(
        refreshToken=refreshToken,
        db=db
    )

@app.post("/logout")
def logout(
    token: str, 
    db: SessionDep
):
    return auth.logout(
        token=token,
        db=db
    )

@app.get("/")
def read_root():
    return {"homePage"}

@app.get("/houses/all")
def getHousesByUser(
    token: str,
    db: SessionDep
):
    return data.house.getHousesByUser(
        str,
        db
    )
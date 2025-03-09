from typing import Union
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from db import SessionDep
from auth import auth
from objects.user import User,UserBase, UserAuthSuccess
from fastapi.middleware.cors import CORSMiddleware
import service.assignment
import service.auth
import service.house
import service.taxrecord
import service.user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service.assignment.router)
app.include_router(service.house.router)
app.include_router(service.taxrecord.router)
app.include_router(service.auth.router)
app.include_router(service.user.router)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
def read_root():
    return {"homePage"}
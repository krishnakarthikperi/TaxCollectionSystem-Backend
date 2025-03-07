from typing import List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
# from objects.assignment import Assignment

class UserBase(SQLModel):
    name: str
    phone: int
    username: str = Field(
        index=True, 
        unique=True, 
        primary_key=True
    )
    userRole: str

class User(UserBase, table=True):
    password: str = Field(
        unique=True
    )
    # assignments: List[Assignment] = Relationship(back_populates="volunteer")

class UserAuthSuccess(UserBase):
    accessToken: str
    refreshToken: str
    tokenType:str = "bearer"  
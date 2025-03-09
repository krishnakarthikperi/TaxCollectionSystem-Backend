from typing import List, TYPE_CHECKING
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

if TYPE_CHECKING:
    from objects.assignment import Assignment

class UserBase(SQLModel):
    name: str
    phone: int
    username: str = Field(
        index=True, 
        unique=True, 
        primary_key=True
    )
    userRole: str | None

class User(UserBase, table=True):
    password: str = Field(
        unique=True
    )
    assignments: List["Assignment"] = Relationship(back_populates="user")

class UserAuthSuccess(UserBase):
    access_token: str
    refresh_token: str
    token_type:str = "Bearer"  
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .house import House as house
from .user import User as user

class AssignmentBase(SQLModel):
    pass

class Assignment(AssignmentBase,table = True):
    id : int = Field(primary_key = True)
    houseId : int = Field(foreign_key = "house.houseNumber")
    username : int = Field(foreign_key = "user.username")
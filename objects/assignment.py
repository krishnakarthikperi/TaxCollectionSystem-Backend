from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from .house import House
from .user import User as user

class AssignmentBase(SQLModel):
    houseId : int = Field(foreign_key = "house.houseNumber")
    username : int = Field(foreign_key = "user.username")

class Assignment(AssignmentBase,table = True):
    id : int = Field(primary_key = True)
    # volunteer: Optional[user] = Relationship(back_populates="assignments")
    # house: Optional[House] = Relationship(back_populates="volunteerAssignments")

class assignmentPOST(AssignmentBase):
    pass

class assignmentGET(AssignmentBase):
    pass
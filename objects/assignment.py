from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

if TYPE_CHECKING:
    from .house import House
    from .user import User

class AssignmentBase(SQLModel):
    houseId : str = Field(foreign_key = "house.houseNumber")
    username : str = Field(foreign_key = "user.username")

class Assignment(AssignmentBase,table = True):
    id : int = Field(primary_key = True)
    user: Optional["User"] = Relationship(back_populates="assignments")
    house: Optional["House"] = Relationship(back_populates="collectorAssignments")

class AssignmentPOSTRequest(AssignmentBase):
    pass

class AssignmentPOSTResponse(AssignmentBase):
    pass

class AssignmentGETRequest(AssignmentBase):
    pass

class AssignmentGETResponse(AssignmentBase):
    pass
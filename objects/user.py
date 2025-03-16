from typing import List, TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship

from objects.assignment import AssignmentGETResponse
from objects.taxrecord import TaxRecordGETResponse


if TYPE_CHECKING:
    from objects.assignment import Assignment
    from objects.taxrecord import TaxRecord

class UserBase(SQLModel):
    name: str
    phone: int
    username: str = Field(
        index=True, 
        primary_key=True
    )
    userRole: str | None

class User(UserBase, table=True):
    password: str = Field(
        unique=True
    )
    assignments: List["Assignment"] = Relationship(back_populates="user")
    taxRecords: List["TaxRecord"] = Relationship(back_populates="collector")

class UserAuthSuccess(UserBase):
    access_token: str
    refresh_token: str
    token_type:str = "Bearer"  

class UserGetResponse(UserBase):
    pass
    # assignments: Optional["AssignmentGETResponse"] | Optional["Assignment"] | None
    # taxRecords: Optional["TaxRecordGETResponse"] | Optional["TaxRecord"] | None
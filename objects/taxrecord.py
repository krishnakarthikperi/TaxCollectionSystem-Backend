from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .house import House
    from .house import House
    from .user import User

class TaxRecordBase(SQLModel):
    amount : float

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    houseId : str = Field(foreign_key = "house.houseNumber")
    collectorId : int = Field(foreign_key = "user.username")
    date : datetime | None = Field(default=datetime.now(timezone.utc))
    collector: Optional["User"] = Relationship(back_populates="taxRecords")
    household: Optional["House"] = Relationship(back_populates="taxRecords")

class TaxRecordGETRequest(TaxRecordBase):
    id: int
    houseId: int
    collectorId: str
    date: datetime

class TaxRecordGETResponse(TaxRecordBase):
    id: int
    houseId: int
    collectorId: str
    date: datetime

class TaxRecordPOSTRequest(TaxRecordBase):
    collectorId: str
    date: datetime

class TaxRecordPOSTResponse(TaxRecordBase):
    collectorId: str
    date: datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .house import House as house
from .user import User as user
from datetime import datetime, timezone

class TaxRecordBase(SQLModel):
    amount : float

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    houseId : int = Field(foreign_key = "house.houseNumber")
    collectorId : int = Field(foreign_key = "user.username")
    date : datetime | None = Field(default=datetime.now(timezone.utc))

class TaxRecordGETRequest(TaxRecordBase):
    id: int
    houseId: int
    collectorId: int
    date: datetime

class TaxRecordPOSTRequest(TaxRecordBase):
    collectorId: int
    date: datetime
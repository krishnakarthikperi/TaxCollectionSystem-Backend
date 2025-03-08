from sqlmodel import Field, Session, SQLModel, create_engine, select
from .house import House as house
from .user import User as user
import datetime

class TaxRecordBase(SQLModel):
    amount : float

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    houseId : int = Field(foreign_key = "house.houseNumber")
    collectorId : int = Field(foreign_key = "user.username")
    date : datetime.datetime | None = Field(default=datetime.datetime.utcnow)

class TaxRecordGETRequest(TaxRecordBase):
    id: int
    houseId: int
    collectorId: int
    date: datetime.datetime

class TaxRecordPOSTRequest(TaxRecordBase):
    collectorId: int
    date: datetime.datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .house import House
from .user import User
import datetime

class TaxRecordBase(SQLModel):
    amount : float

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    houseId : int = Field(foreign_key = "House.houseNumber")
    collectorId : int = Field(foreign_key = "User.username")
    date : datetime.datetime | None = Field(default=datetime.datetime.utcnow)

class TaxRecordGET(TaxRecordBase):
    id: int
    houseId: int
    collectorId: int
    date: datetime

class TaxRecordPOST(TaxRecordBase):
    collectorId: int
    date: datetime
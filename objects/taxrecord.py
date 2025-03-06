from sqlmodel import Field, Session, SQLModel, create_engine, select
from .house import House
import datetime

class TaxRecordBase(SQLModel):
    pass

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    houseId : int = Field(foreign_key = "house.houseNumber")
    date : datetime.datetime | None = Field(default=datetime.datetime.utcnow)
    amount : float
from typing import TYPE_CHECKING, Optional
from sqlmodel import Column, DateTime, Field, Relationship, Session, SQLModel, create_engine, select, text
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .house import House
    from .house import House
    from .user import User

class TaxRecordBase(SQLModel):
    amount : float
    houseId : str = Field(foreign_key = "house.houseNumber")
    collectorId : str = Field(foreign_key = "user.username")

class TaxRecord(TaxRecordBase,table = True):
    id : int = Field(primary_key = True)
    dateCreated : datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    dateUpdated: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        }
    )
    collector: Optional["User"] = Relationship(back_populates="taxRecords")
    household: Optional["House"] = Relationship(back_populates="taxRecords")

class TaxRecordGETRequest(TaxRecordBase):
    pass

class TaxRecordGETResponse(TaxRecordBase):
    id: int
    pass

class TaxRecordPOSTRequest(TaxRecordBase):
    pass

class TaxRecordPOSTResponse(TaxRecordBase):
    id: int
    pass

class TaxRecordPUTRequest(SQLModel):
    id: Optional[int] = None
    amount: float | None

class TaxRecordPUTResponse(TaxRecordBase):
    id: int
    dateUpdated : datetime = datetime.now(timezone.utc)
    pass
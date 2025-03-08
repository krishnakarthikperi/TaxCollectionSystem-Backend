from typing import List, TYPE_CHECKING
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

if TYPE_CHECKING:
    from objects.assignment import Assignment

class HouseBase(SQLModel):
    pass

class HousePOSTRequest(HouseBase):
    assessmentNumber: int = Field(
        index = True,
        unique = True,
        primary_key= True
    )
    houseNumber: str = Field(
        index=True, 
        unique=True 
    )
    houseValue: float | None
    houseTax: float | None
    waterTax: float | None
    libraryTax: float | None
    lightingTax: float | None
    drianageTax: float | None
    husbandOrFatherNameOfOwner: str | None
    ownerName: str | None = Field(
        index = True
    )

class House(HousePOSTRequest, table = True):
    collectorAssignments: List["Assignment"] = Relationship(back_populates="house")

class HouseGETRequest(HouseBase):
    houseNumber: str

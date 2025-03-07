from typing import List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
# from objects.assignment import Assignment

class HouseBase(SQLModel):
    pass

class House(HouseBase, table= True):
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
    # volunteerAssignments: List[Assignment] = Relationship(back_populates="house")

class HousePOST(House):
    pass

class HouseGET(HouseBase):
    houseNumber: str
    pass
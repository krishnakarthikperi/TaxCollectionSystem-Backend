from sqlmodel import Field, Session, SQLModel, create_engine, select

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

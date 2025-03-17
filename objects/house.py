"""
This module defines the data models and schemas for representing a `House` entity in the tax collection system.
Classes:
    - HouseBase: A base class for the `House` model.
    - HousePOSTRequest: Represents the schema for creating a new house record.
        Attributes:
            - assessmentNumber (int): The unique assessment number of the house.
            - houseNumber (str): The unique house number.
            - houseValue (float | None): The value of the house.
            - houseTax (float | None): The tax amount for the house.
            - waterTax (float | None): The water tax amount for the house.
            - libraryTax (float | None): The library tax amount for the house.
            - lightingTax (float | None): The lighting tax amount for the house.
            - drianageTax (float | None): The drainage tax amount for the house.
            - husbandOrFatherNameOfOwner (str | None): The name of the husband or father of the house owner.
            - ownerName (str | None): The name of the house owner.
    - House: Represents the `House` database model.
        Attributes:
            - collectorAssignments (List["Assignment"]): A list of assignments related to the house.
            - taxRecords (List["TaxRecord"]): A list of tax records associated with the house.
    - HouseGETRequest: Represents the schema for retrieving a house record.
        Attributes:
            - houseNumber (str): The unique house number.
    - HouseGETResponse: Represents the schema for responding with house details.
        Attributes:
            - collectorAssignments (List[AssignmentGETRequest] | None): A list of assignment details related to the house.
            - taxRecords (List[TaxRecordGETResponse] | None): A list of tax record details associated with the house.
            - users (List[UserGetResponse] | None): A list of user details associated with the house.
Relationships:
    - The `House` model has relationships with `Assignment` and `TaxRecord` models.
"""

from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from objects.assignment import AssignmentGETRequest
from objects.taxrecord import TaxRecordGETResponse
from objects.user import UserGetResponse

if TYPE_CHECKING:
    from objects.assignment import Assignment
    from objects.taxrecord import TaxRecord

class HouseBase(SQLModel):
    """
    HouseBase is a base model class that inherits from SQLModel.
    It serves as the foundation for defining database models related to houses
    in the tax collection project.

    Attributes:
        (No attributes are currently defined in this base class. Extend this class to add specific fields.)
    """
    pass

class HousePOSTRequest(HouseBase):
    """
    HousePOSTRequest is a data model class that inherits from HouseBase. It represents
    the structure of a POST request for creating or updating house-related information.
    Attributes:
        assessmentNumber (int): The unique assessment number for the house. Acts as a
            primary key and is indexed.
        houseNumber (str): The unique house number. Indexed and must be unique.
        houseValue (float | None): The monetary value of the house. Optional.
        houseTax (float | None): The tax amount applicable to the house. Optional.
        waterTax (float | None): The water tax applicable to the house. Optional.
        libraryTax (float | None): The library tax applicable to the house. Optional.
        lightingTax (float | None): The lighting tax applicable to the house. Optional.
        drianageTax (float | None): The drainage tax applicable to the house. Optional.
        husbandOrFatherNameOfOwner (str | None): The name of the husband or father of the
            house owner. Optional.
        ownerName (str | None): The name of the house owner. Indexed and optional.
    """

    assessmentNumber: int = Field(
        index = True,
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
    """
    Represents a House entity with relationships to assignments and tax records.
    Attributes:
        collectorAssignments (List["Assignment"]): A list of assignments associated with the house.
            This establishes a relationship where assignments are linked back to the house.
        taxRecords (List["TaxRecord"]): A list of tax records associated with the household.
            This establishes a relationship where tax records are linked back to the household.
    """

    collectorAssignments: List["Assignment"] = Relationship(back_populates="house")
    taxRecords: List["TaxRecord"] = Relationship(back_populates="household")

class HouseGETRequest(HouseBase):
    """
    Represents a GET request for retrieving house information.
    Attributes:
        houseNumber (str): The unique identifier or number of the house.
    """

    houseNumber: str

class HouseGETResponse(HousePOSTRequest):    
    """
    HouseGETResponse is a data model that extends the HousePOSTRequest class
    to include additional information about a house, such as collector assignments,
    tax records, and associated users.
    Attributes:
        collectorAssignments (List[AssignmentGETRequest] | None): A list of assignments
            for tax collectors related to the house. Can be None if no assignments exist.
        taxRecords (List[TaxRecordGETResponse] | None): A list of tax records associated
            with the house. Can be None if no tax records exist.
        users (List[UserGetResponse] | None): A list of users associated with the house.
            Can be None if no users are linked to the house.
    """

    collectorAssignments: List[AssignmentGETRequest] | None
    taxRecords: List[TaxRecordGETResponse] | None
    users: List[UserGetResponse] | None

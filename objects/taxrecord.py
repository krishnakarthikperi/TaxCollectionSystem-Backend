"""
This module defines the `TaxRecord` model and its related request and response schemas for managing tax records.
Classes:
    TaxRecordBase(SQLModel):
        Base model for tax records containing common fields.
    TaxRecord(TaxRecordBase, table=True):
        Represents a tax record in the database with additional metadata fields.
    TaxRecordGETRequest(TaxRecordBase):
        Schema for GET requests to retrieve tax records.
    TaxRecordGETResponse(TaxRecordBase):
        Schema for GET responses containing tax record details.
    TaxRecordPOSTRequest(TaxRecordBase):
        Schema for POST requests to create a new tax record.
    TaxRecordPOSTResponse(TaxRecordBase):
        Schema for POST responses containing the created tax record details.
    TaxRecordPUTRequest(SQLModel):
        Schema for PUT requests to update an existing tax record.
    TaxRecordPUTResponse(TaxRecordBase):
        Schema for PUT responses containing the updated tax record details.
Attributes:
    amount (float):
        The amount of tax collected.
    houseId (str):
        Foreign key referencing the house associated with the tax record.
    collectorId (str):
        Foreign key referencing the user who collected the tax.
    id (int):
        Primary key for the tax record.
    dateCreated (datetime):
        Timestamp indicating when the tax record was created.
    dateUpdated (datetime):
        Timestamp indicating when the tax record was last updated.
    collector (Optional["User"]):
        Relationship to the `User` model representing the tax collector.
    household (Optional["House"]):
        Relationship to the `House` model representing the associated household.
"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, text
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .house import House
    from .house import House
    from .user import User

class TaxRecordBase(SQLModel):
    """
    TaxRecordBase is a data model representing a tax record in the system.

    Attributes:
        amount (float): The amount of tax collected.
        houseId (str): The identifier for the house associated with the tax record.
            This is a foreign key referencing the "houseNumber" field in the "house" table.
        collectorId (str): The identifier for the user who collected the tax.
            This is a foreign key referencing the "username" field in the "user" table.
    """
    amount : float
    houseId : str = Field(foreign_key = "house.houseNumber")
    collectorId : str = Field(foreign_key = "user.username")

class TaxRecord(TaxRecordBase,table = True):
    """
    Represents a tax record in the system.

    Attributes:
        id (int): The primary key identifier for the tax record.
        dateCreated (datetime): The timestamp when the tax record was created. Defaults to the current UTC time.
        dateUpdated (datetime): The timestamp when the tax record was last updated. Defaults to the current timestamp in the database.
        collector (Optional[User]): The user who collected the tax. This is a relationship to the User model.
        household (Optional[House]): The household associated with the tax record. This is a relationship to the House model.
    """
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
    """
    Represents a GET request for retrieving tax record information.

    This class inherits from `TaxRecordBase` and serves as a placeholder
    for handling GET requests related to tax records. Additional attributes
    or methods can be added as needed to extend its functionality.
    """
    pass

class TaxRecordGETResponse(TaxRecordBase):
    """
    Represents the response model for retrieving a tax record.

    This class extends the `TaxRecordBase` and includes additional
    fields specific to the GET response.

    Attributes:
        id (int): The unique identifier of the tax record.
    """
    id: int
    pass

class TaxRecordPOSTRequest(TaxRecordBase):
    """
    Represents a POST request for creating or submitting a tax record.

    This class inherits from `TaxRecordBase` and is used to define the structure
    or behavior specific to POST requests for tax records. Additional attributes
    or methods can be added as needed to handle POST-specific logic.

    Note:
        Currently, this class does not add any additional functionality to
        `TaxRecordBase`.
    """
    pass

class TaxRecordPOSTResponse(TaxRecordBase):
    """
    Represents the response object for a POST request related to a tax record.

    Attributes:
        id (int): The unique identifier for the tax record.
    """
    id: int
    pass

class TaxRecordPUTRequest(SQLModel):
    """
    Represents a PUT request payload for updating a tax record.

    Attributes:
        id (Optional[int]): The unique identifier of the tax record. Defaults to None.
        amount (float | None): The amount associated with the tax record. Can be None.
    """
    id: Optional[int] = None
    amount: float | None

class TaxRecordPUTResponse(TaxRecordBase):
    """
    Represents the response object for a PUT operation on a tax record.

    Attributes:
        id (int): The unique identifier of the tax record.
        dateUpdated (datetime): The timestamp indicating when the tax record was last updated.
            Defaults to the current UTC time.
    """
    id: int
    dateUpdated : datetime = datetime.now(timezone.utc)
    pass

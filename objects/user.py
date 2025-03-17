"""
This module defines the User-related models and their relationships for the Tax Collection project.
Classes:
    UserBase(SQLModel):
        A base model for user-related data, containing common fields such as name, phone, username, and userRole.
    User(UserBase, table=True):
        Represents a user entity in the database, extending UserBase with additional fields like password and relationships to assignments and tax records.
    UserAuthSuccess(UserBase):
        Represents the response model for successful user authentication, including access and refresh tokens.
    UserPOSTRequest(UserBase):
        Represents the request model for creating a new user, extending UserBase with a password field.
    UserPOSTResponse(UserBase):
        Represents the response model for a successful user creation, inheriting fields from UserBase.
    UserGetResponse(UserBase):
        Represents the response model for retrieving user details, inheriting fields from UserBase.
Relationships:
    - User has a one-to-many relationship with Assignment, represented by the `assignments` field.
    - User has a one-to-many relationship with TaxRecord, represented by the `taxRecords` field.
Imports:
    - List, TYPE_CHECKING, Optional: Used for type annotations and conditional imports.
    - Field, SQLModel, Relationship: Used for defining SQLModel fields and relationships.
    - AssignmentGETResponse, TaxRecordGETResponse: Used for type hinting in response models.
"""

from typing import List, TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from objects.assignment import AssignmentGETResponse
from objects.taxrecord import TaxRecordGETResponse


if TYPE_CHECKING:
    from objects.assignment import Assignment
    from objects.taxrecord import TaxRecord

class UserBase(SQLModel):
    """
    UserBase is a model class that represents a user in the system.

    Attributes:
        name (str): The name of the user.
        phone (int): The phone number of the user.
        username (str): The unique username of the user, which serves as the primary key and is indexed for efficient querying.
        userRole (str | None): The role of the user in the system, which is optional.
    """
    name: str
    phone: int
    username: str = Field(
        index=True, 
        primary_key=True
    )
    userRole: str | None

class User(UserBase, table=True):
    """
    Represents a User entity in the tax collection system.

    Attributes:
        password (str): The password associated with the user.
        assignments (List[Assignment]): A list of assignments associated with the user.
            This establishes a relationship with the Assignment entity, where the
            "user" attribute in Assignment is the back reference.
        taxRecords (List[TaxRecord]): A list of tax records collected by the user.
            This establishes a relationship with the TaxRecord entity, where the
            "collector" attribute in TaxRecord is the back reference.
    """
    password: str
    assignments: List["Assignment"] = Relationship(back_populates="user")
    taxRecords: List["TaxRecord"] = Relationship(back_populates="collector")

class UserAuthSuccess(UserBase):
    """
    Represents a successful user authentication response.

    Attributes:
        access_token (str): The token used to access protected resources.
        refresh_token (str): The token used to obtain a new access token when the current one expires.
        token_type (str): The type of the token, default is "Bearer".
    """
    access_token: str
    refresh_token: str
    token_type:str = "Bearer"  

class UserPOSTRequest(UserBase):
    """
    Represents a POST request payload for creating a new user.

    Attributes:
        password (str): The password for the user. This should be stored securely and not exposed in plain text.
    """
    password: str    

class UserPOSTResponse(UserBase):
    """
    Represents the response object for a POST request related to a User.

    This class inherits from `UserBase` and does not add any additional
    attributes or methods. It serves as a placeholder for future extensions
    or to provide a clear distinction in the codebase for POST response objects.
    """
    pass    

class UserGetResponse(UserBase):
    """
    Represents the response object for retrieving user information.

    This class is a subclass of `UserBase` and is used to define the structure
    of the data returned when fetching user details. It may include optional
    fields for assignments and tax records, which can be instances of their
    respective response models or domain models.

    Attributes:
        assignments (Optional[AssignmentGETResponse | Assignment | None]):
            The assignments associated with the user, if any.
        taxRecords (Optional[TaxRecordGETResponse | TaxRecord | None]):
            The tax records associated with the user, if any.
    """
    pass
    # assignments: Optional["AssignmentGETResponse"] | Optional["Assignment"] | None
    # taxRecords: Optional["TaxRecordGETResponse"] | Optional["TaxRecord"] | None

"""
This module defines the `Assignment` model and related classes for managing assignments
between users and houses in a tax collection system.
Classes:
    AssignmentBase(SQLModel):
        A base model that defines the common fields for assignments, including `houseId`
        and `username`, which are foreign keys referencing the `House` and `User` models.
    Assignment(AssignmentBase, table=True):
        Represents the database table for assignments. Includes an auto-incrementing
        primary key `id` and relationships to the `User` and `House` models.
    AssignmentPOSTRequest(AssignmentBase):
        A model for handling POST requests when creating a new assignment. Inherits
        fields from `AssignmentBase`.
    AssignmentPOSTResponse(AssignmentBase):
        A model for structuring the response of a POST request when an assignment is
        successfully created. Inherits fields from `AssignmentBase`.
    AssignmentGETRequest(AssignmentBase):
        A model for handling GET requests when querying assignments. Inherits fields
        from `AssignmentBase`.
    AssignmentGETResponse(AssignmentBase):
        A model for structuring the response of a GET request when retrieving assignment
        data. Inherits fields from `AssignmentBase`.
Attributes:
    TYPE_CHECKING (bool):
        A flag used to enable type checking for forward references to the `House` and
        `User` models during static analysis.
Relationships:
    - `Assignment.user`: Establishes a relationship with the `User` model, allowing
      access to the user associated with an assignment.
    - `Assignment.house`: Establishes a relationship with the `House` model, allowing
      access to the house associated with an assignment.
"""

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .house import House
    from .user import User

class AssignmentBase(SQLModel):
    """
    AssignmentBase is a model class that represents the assignment of a user to a house.
    Attributes:
        houseId (str): A foreign key referencing the houseNumber field in the house table.
        username (str): A foreign key referencing the username field in the user table.
    """

    houseId : str = Field(foreign_key = "house.houseNumber")
    username : str = Field(foreign_key = "user.username")

class Assignment(AssignmentBase,table = True):
    """
    Represents an assignment entity that links a user to a house for tax collection purposes.

    Attributes:
        id (int): The primary key identifier for the assignment.
        user (Optional["User"]): The user associated with this assignment. This establishes a relationship
            with the User model and allows back-population of assignments.
        house (Optional["House"]): The house associated with this assignment. This establishes a relationship
            with the House model and allows back-population of collector assignments.
    """
    id : int = Field(primary_key = True)
    user: Optional["User"] = Relationship(back_populates="assignments")
    house: Optional["House"] = Relationship(back_populates="collectorAssignments")

class AssignmentPOSTRequest(AssignmentBase):
    """
    Represents a POST request for creating or updating an assignment.

    This class inherits from `AssignmentBase` and can be extended to include
    additional attributes or methods specific to handling POST requests for
    assignments.
    """
    pass

class AssignmentPOSTResponse(AssignmentBase):
    """
    Represents the response object for a POST request related to an assignment.

    This class inherits from `AssignmentBase` and does not introduce any additional
    attributes or methods. It serves as a placeholder for potential future extensions
    or customizations specific to POST responses.

    Attributes:
        Inherits all attributes from `AssignmentBase`.
    """
    pass

class AssignmentGETRequest(AssignmentBase):
    """
    Represents a GET request for an assignment.
    This class is a placeholder for handling GET requests related to assignments.
    It inherits from `AssignmentBase` and can be extended with additional
    attributes or methods specific to GET request handling.
    Attributes:
        (No specific attributes are defined yet; inherits all attributes from `AssignmentBase`.)
    """
    pass

class AssignmentGETResponse(AssignmentBase):
    """
    Represents the response object for a GET request related to an assignment.
    This class inherits from `AssignmentBase` and can be extended to include
    additional attributes or methods specific to the GET response for assignments.
    """

    pass

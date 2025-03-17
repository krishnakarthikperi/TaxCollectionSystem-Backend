"""
This module defines SQLModel-based classes for managing tokens in the tax collection system.
Classes:
    RevokedToken: Represents a revoked token with a unique identifier (JTI) stored in the database.
    RefreshTokenPOSTRequest: Represents a request model for refreshing tokens, containing the refresh token.
Dependencies:
    - sqlmodel: Used for defining database models and fields.
"""

from sqlmodel import Field, SQLModel

class RevokedToken(SQLModel, table=True):
    """
    Represents a revoked token in the system.

    This model is used to store JSON Web Token Identifiers (JTIs) that have been
    revoked, preventing their further use for authentication or authorization.

    Attributes:
        jti (str): The unique identifier of the JSON Web Token (JWT) that has been revoked.
    """
    jti : str = Field(primary_key=True)

class RefreshTokenPOSTRequest(SQLModel):
    """
    Represents a POST request model for refreshing an authentication token.

    Attributes:
        refresh_token (str): The refresh token used to obtain a new access token.
    """
    refresh_token: str

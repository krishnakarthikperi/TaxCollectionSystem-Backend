"""
This module provides utility functions for password hashing and verification
using the `passlib` library.
Functions:
    hashPassword(password: str) -> str:
        Hashes a plain text password using the bcrypt algorithm.
    verifyPassword(plain_password: str, hashed_password: str) -> bool:
        Verifies a plain text password against a hashed password.
Dependencies:
    - passlib.context.CryptContext: Used for password hashing and verification.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hashPassword(password: str) -> str:
    """
    Hashes a plaintext password using a secure hashing algorithm.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password as a string.
    """
    return pwd_context.hash(password)


def verifyPassword(
    plain_password,
    hashed_password,
):
    """
    Verifies if a plain text password matches a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

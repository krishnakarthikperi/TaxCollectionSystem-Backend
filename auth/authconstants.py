"""
This module defines constants used for authentication and token management.

Constants:
    ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
    ALGORITHM (str): The algorithm used for encoding and decoding tokens.
    REFRESH_SECRET_KEY (str): The secret key used for signing refresh tokens.
        (Note: Replace with a secure key before deployment.)
    REFRESH_TOKEN_EXPIRE_DAYS (int): The expiration time for refresh tokens in days.
    ACCESS_SECRET_KEY (str): The secret key used for signing access tokens.
        (Note: Replace with a secure key before deployment.)
    ACCESS_TOKEN_TYPE (str): The type identifier for access tokens.
    REFRESH_TOKEN_TYPE (str): The type identifier for refresh tokens.
"""

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
REFRESH_SECRET_KEY = "your_refresh_secret_key" # Change this!
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_SECRET_KEY = "your_secret_key"  # Change this!
ACCESS_TOKEN_TYPE = "ACCESS"
REFRESH_TOKEN_TYPE = "REFRESH"

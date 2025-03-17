"""
This module defines a collection of constant string values used throughout the
Tax Collection service. These constants are primarily used for error messages,
user roles, and validation responses.
Constants:
----------
- COULD_NOT_VALIDATE_CREDENTIALS: Error message for failed credential validation.
- TOKEN_EXPIRED: Error message for expired tokens.
- INVALID_CREDENTIALS: Error message for incorrect username or password.
- USER_NOT_FOUND: Error message when a user is not found in the system.
- INVALID_TOKEN: Error message for invalid tokens.
- INVALID_REFRESH_TOKEN: Error message for invalid refresh tokens.
- LOGGED_OUT_SUCCESSFULLY: Message indicating successful logout.
- INSUFFICIENT_PERMISSIONS: Error message for insufficient user permissions.
- USER_ROLE_ADMIN: Represents the "ADMIN" user role.
- USER_ROLE_COLLECTOR: Represents the "COLLECTOR" user role.
- INVALID_VOLUNTEER_DETAILS: Error message for invalid volunteer details.
- INVALID_HOUSE_NUMBER: Error message for invalid house numbers.
- ONLY_COLLECTORS_RECORD_TAX_COLLECTION: Error message when non-collectors attempt to record tax collection.
- INCORRECT_HOUSE_MAPPING: Error message for incorrect house-to-user mapping.
- RECORD_NOT_FOUND: Error message when a record is not found.
- USERNAME_ALREADY_REGISTERED: Error message when a username is already registered.
"""

COULD_NOT_VALIDATE_CREDENTIALS:str = "Could not validate credentials"
TOKEN_EXPIRED:str = "Token expired"
INVALID_CREDENTIALS:str = "Incorrect username or password"
USER_NOT_FOUND:str = "User not found"
INVALID_TOKEN:str = "Invalid token"
INVALID_REFRESH_TOKEN:str = "Invalid refresh token"
LOGGED_OUT_SUCCESSFULLY:str = "Logged out successfully"
INSUFFICIENT_PERMISSIONS:str = "Not enough permissions"
USER_ROLE_ADMIN:str = "ADMIN"
USER_ROLE_COLLECTOR:str = "COLLECTOR"
INVALID_VOLUNTEER_DETAILS:str = "Invalid volunteer details"
INVALID_HOUSE_NUMBER:str = "Invalid house number"
ONLY_COLLECTORS_RECORD_TAX_COLLECTION:str = "Only collectors can record tax collection"
INCORRECT_HOUSE_MAPPING:str = "You are not assigned to this household"
RECORD_NOT_FOUND:str = "Record not found"
USERNAME_ALREADY_REGISTERED:str = "Username already registered"

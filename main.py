"""
Main module for the Tax Collection application.
This module initializes the FastAPI application, configures middleware, and includes routers for various services.
Modules and Dependencies:
- FastAPI: Used to create the web application.
- SQLModel: Provides ORM functionality for database interactions.
- FastAPI Middleware: Configures Cross-Origin Resource Sharing (CORS) settings.
- Service Modules: Includes routers for assignment, house, tax record, authentication, and user management.
Routes:
- Root ("/"): Returns a simple homepage response.
Middleware:
- CORS Middleware: Configured to allow all origins, credentials, methods, and headers. Update `allow_origins` for specific domains in production.
Routers:
- `service.assignment.router`: Handles assignment-related routes.
- `service.house.router`: Handles house-related routes.
- `service.taxrecord.router`: Handles tax record-related routes.
- `service.auth.router`: Handles authentication-related routes.
- `service.user.router`: Handles user-related routes.
Note:
- The `on_startup` event for database initialization is commented out. Uncomment and implement `create_db_and_tables` if needed.
"""

import os
import sys
from typing import Union
from fastapi import FastAPI, Depends
import pytest
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn
from db import SessionDep
from auth import auth
from objects.user import User,UserBase, UserAuthSuccess
from fastapi.middleware.cors import CORSMiddleware
import service.assignment
import service.auth
import service.house
import service.taxrecord
import service.user
import logging

from service.assignment import router as assignment_router
from service.house import router as house_router
from service.taxrecord import router as taxrecord_router
from service.auth import router as auth_router
from service.user import router as user_router

logging.basicConfig(level=logging.DEBUG)
logging.debug("Initializing application...")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assignment_router)
app.include_router(house_router)
app.include_router(taxrecord_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    """
    Handles the root endpoint of the application.

    Returns:
        dict: A dictionary containing the homepage information.
    """
    return {"message": "Welcome to the Tax Collection System"}


def run_tests():
    """
    Runs all tests in the `tests` folder using pytest.
    If any test fails, the application will exit with a non-zero status code.
    """
    logging.debug("Running tests...")
    if getattr(sys, "frozen", False):  # Check if running inside PyInstaller
        # Use the PyInstaller's bundled directory
        tests_path = os.path.join(sys._MEIPASS, "tests")
    else:
        # Use the normal project directory
        tests_path = os.path.abspath("tests")

    # Run pytest on the tests directory
    result = pytest.main(["-v", tests_path, f"--rootdir={tests_path}"])
    if result != 0:
        logging.error("Tests failed. Exiting application.")
        sys.exit(1)
    logging.debug("All tests passed successfully.")


if __name__ == "__main__":
    # Run tests before starting the server
    run_tests()
    # Start the Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)

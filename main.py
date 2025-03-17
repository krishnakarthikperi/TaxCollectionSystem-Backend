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

from typing import Union
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from db import SessionDep
from auth import auth
from objects.user import User,UserBase, UserAuthSuccess
from fastapi.middleware.cors import CORSMiddleware
import service.assignment
import service.auth
import service.house
import service.taxrecord
import service.user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service.assignment.router)
app.include_router(service.house.router)
app.include_router(service.taxrecord.router)
app.include_router(service.auth.router)
app.include_router(service.user.router)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
def read_root():
    """
    Handles the root endpoint of the application.

    Returns:
        dict: A dictionary containing the homepage information.
    """
    return {"homePage"}

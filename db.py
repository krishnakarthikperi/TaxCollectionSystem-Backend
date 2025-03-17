"""
This module sets up the database connection and provides utility functions for
managing the database and sessions in a FastAPI application.
Functions:
    createDbAndTables():
        Creates the database and all tables defined in the SQLModel metadata.
    getSession():
        Provides a session object for interacting with the database. This is
        designed to be used as a dependency in FastAPI routes.
Variables:
    sqlite_file_name (str):
        The name of the SQLite database file.
    sqlite_url (str):
        The connection URL for the SQLite database.
    connect_args (dict):
        Connection arguments for the SQLite engine.
    engine (sqlmodel.Engine):
        The SQLAlchemy engine used to connect to the SQLite database.
    SessionDep (Annotated[Session, Depends]):
        A FastAPI dependency that provides a database session.
"""

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import objects

sqlite_file_name = "taxcollection1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args, echo = True)

def createDbAndTables():
    """
    Creates the database and all associated tables defined in the SQLModel metadata.

    This function uses the SQLModel library to initialize the database schema by
    creating all tables defined in the metadata object. It requires a valid database
    engine to be configured and accessible.

    Note:
        Ensure that the `engine` variable is properly initialized with a database
        connection before calling this function.

    Raises:
        Any exceptions raised by `SQLModel.metadata.create_all` if the database
        connection or schema creation fails.
    """
    SQLModel.metadata.create_all(engine)

def getSession():
    """
    Provides a database session using a context manager.

    This function yields a session object connected to the database engine.
    The session is automatically closed when the context manager exits.

    Yields:
        Session: A SQLAlchemy session object for interacting with the database.
    """
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    createDbAndTables()

SessionDep = Annotated[Session, Depends(getSession)]

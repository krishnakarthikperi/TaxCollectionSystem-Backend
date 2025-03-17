"""
Unit tests for the database module.
This module contains tests to verify the functionality of the database-related
functions and configurations in the application.
Functions:
- test_createDbAndTables: Ensures that the database and tables are created
    without raising any exceptions.
- test_getSession: Verifies that the session generator yields a valid session
    instance and that the session can be used.
- test_engine_configuration: Checks that the database engine is configured
    correctly with the expected database name and driver.
"""

from sqlmodel import Session
from db import createDbAndTables, getSession, engine


def test_createDbAndTables():
    """
    GIVEN a function `createDbAndTables` that is responsible for creating a database and its tables,
    WHEN the function is called,
    THEN it should execute without raising any exceptions, ensuring the database and tables are created successfully.
    """
    # Ensure the database and tables are created without errors
    try:
        createDbAndTables()
    except Exception as e:
        assert False, f"createDbAndTables raised an exception: {e}"

def test_getSession():
    """
    GIVEN a session generator function `getSession` that is expected to yield a database session.
    WHEN the function is called and a session is retrieved from the generator.
    THEN ensure that the session is not None, verify that it is an instance of the `Session` class,
        and confirm that the session can be properly closed without errors.
    """
    # Test if the session is created and can be used
    session_generator = getSession()
    session = next(session_generator, None)
    assert session is not None, "getSession did not yield a session"
    assert isinstance(session, Session), "getSession did not yield a valid Session instance"
    session.close()

def test_engine_configuration():
    """
    GIVEN a database engine configured for the application,
    WHEN the engine's configuration is checked,
    THEN it should confirm that the database is set to "taxcollection1.db"
        and the driver is configured to use SQLite.
    """
    # Ensure the engine is configured correctly
    assert engine.url.database == "taxcollection1.db", "Engine is not configured with the correct database"
    assert engine.url.drivername == "sqlite", "Engine is not configured with SQLite"

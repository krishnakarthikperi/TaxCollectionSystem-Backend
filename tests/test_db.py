from sqlmodel import Session
from db import createDbAndTables, getSession, engine


def test_createDbAndTables():
    # Ensure the database and tables are created without errors
    try:
        createDbAndTables()
    except Exception as e:
        assert False, f"createDbAndTables raised an exception: {e}"

def test_getSession():
    # Test if the session is created and can be used
    session_generator = getSession()
    session = next(session_generator, None)
    assert session is not None, "getSession did not yield a session"
    assert isinstance(session, Session), "getSession did not yield a valid Session instance"
    session.close()

def test_engine_configuration():
    # Ensure the engine is configured correctly
    assert engine.url.database == "taxcollection1.db", "Engine is not configured with the correct database"
    assert engine.url.drivername == "sqlite", "Engine is not configured with SQLite"
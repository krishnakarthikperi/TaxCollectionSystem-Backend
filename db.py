from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import objects

sqlite_file_name = "taxcollection1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args, echo = True)

def createDbAndTables():
    SQLModel.metadata.create_all(engine)

def getSession():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    createDbAndTables()

SessionDep = Annotated[Session, Depends(getSession)]
from sqlmodel import Field, Session, SQLModel, create_engine, select

class UserBase(SQLModel):
    name: str
    phone: int

class User(UserBase, table=True):
    username: str = Field(
        index=True, 
        unique=True, 
        primary_key=True
    )
    password: str = Field(
        unique=True
    )
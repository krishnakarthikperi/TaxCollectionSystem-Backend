from sqlmodel import Field, Session, SQLModel, create_engine, select

class UserBase(SQLModel):
    name: str
    phone: int
    username: str = Field(
        index=True, 
        unique=True, 
        primary_key=True
    )

class User(UserBase, table=True):
    password: str = Field(
        unique=True
    )

class UserAuthSuccess(UserBase):
    accessToken: str
    refreshToken: str
    tokenType:str = "bearer"  
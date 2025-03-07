from sqlmodel import Field, Session, SQLModel, create_engine, select

class RevokedToken(SQLModel, table=True):
    jti : str = Field(primary_key=True)
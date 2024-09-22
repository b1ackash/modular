# models.py
from sqlmodel import SQLModel, Field, create_engine

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str  # This will store the hashed password

# Create the database engine
engine = create_engine("sqlite:///database.db")
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float
    is_sold: bool = Field(default=False)

    # foreign key to user table
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# request body for creating a book
class BookCreate(SQLModel):
    title: str
    author: str
    price: float
    user_id: int


# response model for book
class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int


# avoid circular import
from models.user import User

Book.model_rebuild()

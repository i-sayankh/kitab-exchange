from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from database import get_session
from typing import Optional

from models.book import Book, BookCreate, BookRead, BookUpdate

from auth import verify_api_key

book_router = APIRouter(prefix="/books", tags=["Books"])


@book_router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


@book_router.get("/", response_model=list[BookRead])
def list_books(
    title: Optional[str] = Query(default=None, description="Filter books by title"),
    author: Optional[str] = Query(default=None, description="Filter books by author"),
    session: Session = Depends(get_session),
):
    query = select(Book).where(Book.is_sold == False)

    if title:
        query = query.where(Book.contains(title))

    if author:
        query = query.where(Book.contains(author))

    books = session.exec(query).all()
    return books


@book_router.post("/", response_model=BookRead)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    book = Book.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@book_router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_update_data: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    book_data = book_update_data.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@book_router.patch("/{book_id}/sold", response_model=BookRead)
def mark_book_as_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    book.is_sold = True
    session.add(book)
    session.commit()
    session.refresh(book)

    return book

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from app.services import book_service
from app.schemas.book_schema import BookCreate, BookResponse, BookAvailability
from app.config.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {
        "title": title, "author": author,
        "genre": genre, "language": language, "year": year
    }
    active_filters = {k: v for k, v in filters.items() if v is not None}
    books = book_service.filter_books(db, active_filters)

    result = []
    for book in books:
        avail = book_service.get_book_availability(db, book.id)
        result.append(BookResponse(
            **{c.name: getattr(book, c.name) for c in book.__table__.columns},
            availability=BookAvailability(**avail)
        ))
    return result


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = book_service.create_book(db, data)
    avail = book_service.get_book_availability(db, book.id)
    return BookResponse(
        **{c.name: getattr(book, c.name) for c in book.__table__.columns},
        availability=BookAvailability(**avail)
    )
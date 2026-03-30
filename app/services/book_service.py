from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.book_copy import BookCopy, BookStatus
from app.schemas.book_schema import BookCreate
from app.repositories import book_repository
from fastapi import HTTPException

def filter_books(db: Session, filters: dict = None):
    query = db.query(Book)

    if filters:
        for key, value in filters.items():
            if value is None:
                continue
            column = getattr(Book, key, None)
            if column is not None:
                if str(column.type) in ['VARCHAR', 'TEXT', 'String']:
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)
    
    return query.all()


def get_book_availability(db: Session, book_id: int):
    copies = db.query(BookCopy).filter(BookCopy.book_id == book_id).all()

    if not copies:
        return {
            "total": 0,
            "available": 0,
            "borrowed": 0,
            "copies": []
        }

    available_copies_list = [c for c in copies if c.status == BookStatus.AVAILABLE]
    borrowed_count = sum(1 for c in copies if c.status == BookStatus.BORROWED)

    return {
        "total": len(copies),
        "available": len(available_copies_list),
        "borrowed": borrowed_count,
        "copies": available_copies_list 
    }

def create_book(db: Session, data: BookCreate) -> Book:
    if data.isbn:
        existing = book_repository.get_by_isbn(db, data.isbn)
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Book with ISBN {data.isbn} already exists"
            )

    book_data = data.model_dump(exclude={"copies_count"})
    book = Book(**book_data)

    book_repository.create_book(db, book)
    book_repository.create_book_copies(db, book.id, data.copies_count)

    db.commit()
    db.refresh(book)

    return book
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.book_copy import BookCopy, BookStatus

def get_by_isbn(db: Session, isbn: str):
    return db.query(Book).filter(Book.isbn == isbn).first()

def create_book(db: Session, book: Book) -> Book:
    db.add(book)
    db.flush()  # gets us the book.id without committing
    return book

def create_book_copies(db: Session, book_id: int, count: int):
    copies = []
    for _ in range(count):
        copy = BookCopy(
            book_id=book_id,
            status=BookStatus.AVAILABLE
        )
        db.add(copy)
        copies.append(copy)
    return copies
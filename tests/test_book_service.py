import pytest
from fastapi import HTTPException
from app.services.book_service import create_book
from app.schemas.book_schema import BookCreate

def make_book_data(**kwargs):
    defaults = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "isbn": "9780132350884",
        "language": "English",
        "copies_count": 3
    }
    defaults.update(kwargs)
    return BookCreate(**defaults)

# ✅ Happy path
def test_create_book_success(db):
    data = make_book_data()
    book = create_book(db, data)

    assert book.id is not None
    assert book.title == "Clean Code"
    assert book.author == "Robert Martin"

# ✅ Copies created
def test_create_book_creates_copies(db):
    from app.models.book_copy import BookCopy
    data = make_book_data(copies_count=3)
    book = create_book(db, data)

    copies = db.query(BookCopy).filter(BookCopy.book_id == book.id).all()
    assert len(copies) == 3

# ❌ ISBN clash
def test_create_book_duplicate_isbn(db):
    data = make_book_data()
    create_book(db, data)

    with pytest.raises(HTTPException) as exc:
        create_book(db, make_book_data())

    assert exc.value.status_code == 409
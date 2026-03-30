import pytest
from fastapi import HTTPException
from app.services.book_service import create_book
from app.services.borrow_service import borrow_book
from app.services.return_service import return_book
from app.schemas.book_schema import BookCreate
from app.models.user import User, Membership
from app.models.borrow_record import BorrowStatus
from datetime import datetime, timedelta, timezone

def make_user(db, email="test@example.com"):
    user = User(
        first_name="John",
        second_name="Doe",
        email=email,
        membership_type=Membership.standard,
        membership_start=datetime.now(timezone.utc),
        membership_end=datetime.now(timezone.utc) + timedelta(days=365)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def make_book(db, isbn="9780132350884", copies=3):
    data = BookCreate(
        title="Clean Code",
        author="Robert Martin",
        isbn=isbn,
        language="English",
        copies_count=copies
    )
    return create_book(db, data)

# ✅ Happy path
def test_borrow_book_success(db):
    user = make_user(db)
    book = make_book(db)

    record = borrow_book(db, user.id, book.id)

    assert record.id is not None
    assert record.user_id == user.id
    assert record.status == BorrowStatus.BORROWED
    assert record.return_date is None

# ✅ Audit log — dates correct
def test_borrow_record_dates(db):
    user = make_user(db)
    book = make_book(db)

    before = datetime.now(timezone.utc).replace(tzinfo=None)
    record = borrow_book(db, user.id, book.id)
    after = datetime.now(timezone.utc).replace(tzinfo=None)

    assert before <= record.borrow_date <= after
    assert record.due_date > record.borrow_date
    
# ❌ No copies available
def test_borrow_no_copies(db):
    user = make_user(db)
    book = make_book(db, copies=1)

    borrow_book(db, user.id, book.id)  # takes the only copy

    with pytest.raises(HTTPException) as exc:
        borrow_book(db, user.id, book.id)

    assert exc.value.status_code == 404

# ❌ Borrow limit
def test_borrow_limit_enforced(db):
    user = make_user(db)

    # Create 5 books and borrow all of them
    for i in range(5):
        book = make_book(db, isbn=f"isbn-{i}", copies=1)
        borrow_book(db, user.id, book.id)

    # 6th borrow should be rejected
    book6 = make_book(db, isbn="isbn-6", copies=1)
    with pytest.raises(HTTPException) as exc:
        borrow_book(db, user.id, book6.id)

    assert exc.value.status_code == 400

# ✅ Return flow
def test_return_book(db):
    from app.models.book_copy import BookStatus
    user = make_user(db)
    book = make_book(db, copies=1)

    record = borrow_book(db, user.id, book.id)
    returned = return_book(db, record.id)

    assert returned.status == BorrowStatus.RETURNED
    assert returned.return_date is not None
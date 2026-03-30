from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.borrow_record import BorrowRecord, BorrowStatus
from app.models.book_copy import BookCopy, BookStatus

BORROW_LIMIT = 5
BORROW_DAYS = 14

def borrow_book(db: Session, user_id: int, book_id: int) -> BorrowRecord:
    # 1. Check active borrow limit
    active_borrows = db.query(BorrowRecord)\
        .filter(BorrowRecord.user_id == user_id)\
        .filter(BorrowRecord.status == BorrowStatus.BORROWED)\
        .count()
    if active_borrows >= BORROW_LIMIT:
        raise HTTPException(status_code=400, detail="Borrow limit reached")

    # 2. Find available copy
    available_copy = db.query(BookCopy)\
        .filter(BookCopy.book_id == book_id)\
        .filter(BookCopy.status == BookStatus.AVAILABLE)\
        .first()
    if not available_copy:
        raise HTTPException(status_code=404, detail="No available copies")

    # 3. Create borrow record
    record = BorrowRecord(
        user_id=user_id,
        copy_id=available_copy.id,
        borrow_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=BORROW_DAYS),
        status=BorrowStatus.BORROWED
    )
    db.add(record)

    # 4. Mark copy as borrowed
    available_copy.status = BookStatus.BORROWED

    db.commit()
    db.refresh(record)
    return record
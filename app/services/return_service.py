from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.borrow_record import BorrowRecord, BorrowStatus
from app.models.book_copy import BookStatus

def return_book(db: Session, borrow_record_id: int) -> BorrowRecord:
    record = db.query(BorrowRecord)\
        .filter(BorrowRecord.id == borrow_record_id)\
        .first()

    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if record.status != BorrowStatus.BORROWED:
        raise HTTPException(status_code=400, detail=f"Record is already {record.status.value}")

    record.status = BorrowStatus.RETURNED
    record.return_date = datetime.now(timezone.utc)

    if not record.copy:
        raise HTTPException(status_code=500, detail="No associated copy found")

    record.copy.status = BookStatus.AVAILABLE

    db.commit()
    db.refresh(record)
    return record
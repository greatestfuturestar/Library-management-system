from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.borrow_schema import BorrowRequest, BorrowResponse
from app.services.borrow_service import borrow_book
from app.config.database import get_db
from app.services.return_service import return_book
from app.schemas.borrow_schema import BorrowResponse


router = APIRouter(prefix="/borrow", tags=["borrow"])

@router.post("/", response_model=BorrowResponse, status_code=201)
def borrow(data: BorrowRequest, db: Session = Depends(get_db)):
    return borrow_book(db, data.user_id, data.book_id)

@router.post("/return/{borrow_record_id}", response_model=BorrowResponse)
def return_borrowed_book(borrow_record_id: int, db: Session = Depends(get_db)):
    return return_book(db, borrow_record_id)
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.borrow_record import BorrowStatus

class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    copy_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: BorrowStatus

    model_config = ConfigDict(from_attributes=True)
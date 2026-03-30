from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.config.database import Base

class BorrowStatus(enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"

class BorrowRecord(Base):
    __tablename__ =  "borrow_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id	= Column(Integer, ForeignKey("users.id"), nullable=True)
    copy_id	= Column(Integer, ForeignKey("bookcopies.id"), nullable=True)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    status = Column(Enum(BorrowStatus), default=BorrowStatus.BORROWED, nullable=False)

    user = relationship("User", back_populates="borrow_records")
    copy = relationship("BookCopy", back_populates="borrow_records")

    return_date = Column(DateTime, nullable=True) 



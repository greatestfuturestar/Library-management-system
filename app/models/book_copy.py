from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.config.database import Base

class BookStatus(enum.Enum):
    AVAILABLE = 'available'
    BORROWED = 'borrowed'
    LOST = 'lost'


class BookCopy(Base):
    __tablename__ = "bookcopies"


    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    location = Column(String, nullable=True)
    acquisition_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    book = relationship("Book", back_populates="copies")

    borrow_records = relationship("BorrowRecord", back_populates="copy")
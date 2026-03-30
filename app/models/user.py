from sqlalchemy import Column, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.config.database import Base

class Membership(enum.Enum):
    standard = 'standard' 
    premium = 'premium'
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    membership_type = Column(Enum(Membership), default=Membership.standard, nullable=False)
    membership_start =	Column(DateTime, default=datetime.utcnow, nullable=False)
    membership_end  = Column(DateTime, nullable=False)

    borrow_records = relationship("BorrowRecord", back_populates="user")





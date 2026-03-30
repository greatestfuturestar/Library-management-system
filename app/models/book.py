from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.config.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    copies = relationship("BookCopy", back_populates="book")




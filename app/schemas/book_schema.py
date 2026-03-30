from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    language: Optional[str] = "English"
    publisher: Optional[str] = None
    year: Optional[int] = None

class BookAvailability(BaseModel):
    total: int
    available: int
    borrowed: int

class BookCreate(BookBase):
    copies_count: int = 1

class BookResponse(BookBase):
    id: int
    availability: Optional[BookAvailability] = None

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import Membership

class UserCreate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    membership_type: Membership = Membership.standard

class UserResponse(BaseModel):
    id: int
    first_name: str
    second_name: str
    email: str
    membership_type: Membership
    membership_start: datetime
    membership_end: datetime

    model_config = ConfigDict(from_attributes=True)
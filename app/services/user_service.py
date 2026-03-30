from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from app.models.user import User, Membership
from app.schemas.user_schema import UserCreate
from app.repositories import user_repository

MEMBERSHIP_DURATION = {
    Membership.standard: 365,
    Membership.premium: 730
}

def create_user(db: Session, data: UserCreate) -> User:
    existing = user_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    now = datetime.now(timezone.utc)
    duration = MEMBERSHIP_DURATION[data.membership_type]

    user = User(
        first_name=data.first_name,
        second_name=data.second_name,
        email=data.email,
        membership_type=data.membership_type,
        membership_start=now,
        membership_end=now + timedelta(days=duration)
    )

    user_repository.create_user(db, user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> User:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
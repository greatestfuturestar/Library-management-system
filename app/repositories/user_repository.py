from sqlalchemy.orm import Session
from app.models.user import User

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: User) -> User:
    db.add(user)
    return user
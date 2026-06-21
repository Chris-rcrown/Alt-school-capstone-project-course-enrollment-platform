from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.crud import user as user_crud
from app.schemas.user import UserCreate


def register_user(db: Session, user_in: UserCreate):
    existing_user = user_crud.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = security.get_password_hash(user_in.password)
    return user_crud.create_user(db, user_in, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    user = user_crud.get_user_by_email(db, email=email)
    if not user or not security.verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


def create_user_access_token(email: str):
    return security.create_access_token(subject=email)

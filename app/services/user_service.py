from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from repositories.user_repository import user_repository


def get_user(db: Session, user_id: int):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def list_users(db: Session):
    return user_repository.get_all(db)


def create_user(db: Session, data: UserCreate):
    try:
        return user_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user(db, user_id)
    try:
        return user_repository.update(db, user, data.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_repository.delete(db, user)

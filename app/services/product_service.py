from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductUpdate
from repositories.product_repository import product_repository


def get_product(db: Session, product_id: int):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


def list_products(db: Session):
    return product_repository.get_all(db)


def create_product(db: Session, data: ProductCreate):
    try:
        return product_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id or supplier_id. Make sure both exist."
        )


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product(db, product_id)
    try:
        return product_repository.update(
            db, product, data.model_dump(exclude_unset=True)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id or supplier_id. Make sure both exist."
        )


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    product_repository.delete(db, product)
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.sale_item import SaleItemCreate, SaleItemUpdate
from repositories.sale_item_repository import sale_item_repository


def get_sale_item(db: Session, sale_item_id: int):
    sale_item = sale_item_repository.get(db, sale_item_id)
    if not sale_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale item not found"
        )
    return sale_item


def list_sale_items(db: Session):
    return sale_item_repository.get_all(db)


def create_sale_item(db: Session, data: SaleItemCreate):
    try:
        return sale_item_repository.create(db, data.model_dump(by_alias=False, exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sale_id or product_id. Make sure both exist."
        )


def update_sale_item(db: Session, sale_item_id: int, data: SaleItemUpdate):
    sale_item = get_sale_item(db, sale_item_id)
    try:
        return sale_item_repository.update(
            db, sale_item, data.model_dump(exclude_unset=True, by_alias=False)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sale_id or product_id. Make sure both exist."
        )


def delete_sale_item(db: Session, sale_item_id: int):
    sale_item = get_sale_item(db, sale_item_id)
    sale_item_repository.delete(db, sale_item)
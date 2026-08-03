from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class SaleItemBase(BaseModel):
    Sale_id: int
    Product_id: int
    quantity: int
    item_price: Decimal


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    Sale_id: int | None = None
    Product_id: int | None = None
    quantity: int | None = None
    item_price: Decimal | None = None


class SaleItemRead(SaleItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

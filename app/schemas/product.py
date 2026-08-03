from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    barcode: str | None = None
    product_name: str
    unit_price: Decimal
    stock_qty: int = 0
    category_id: int | None = None
    supplier_id: int | None = None
    is_active: bool | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    barcode: str | None = None
    product_name: str | None = None
    unit_price: Decimal | None = None
    stock_qty: int | None = None
    category_id: int 
    supplier_id: int 
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    sale_id: int = Field(alias="Sale_id")
    product_id: int = Field(alias="Product_id")
    quantity: int
    item_price: Decimal

    model_config = ConfigDict(populate_by_name=True)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    sale_id: int | None = Field(default=None, alias="Sale_id")
    product_id: int | None = Field(default=None, alias="Product_id")
    quantity: int | None = None
    item_price: Decimal | None = None

    model_config = ConfigDict(populate_by_name=True)


class SaleItemRead(SaleItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
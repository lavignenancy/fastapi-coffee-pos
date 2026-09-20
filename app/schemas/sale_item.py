from datetime import datetime
from decimal import Decimal
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    sale_id: int = Field(validation_alias=AliasChoices("sale_id", "Sale_id"))
    product_id: int = Field(validation_alias=AliasChoices("product_id", "Product_id"))
    quantity: int
    item_price: Decimal

    model_config = ConfigDict(populate_by_name=True)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    sale_id: int | None = Field(default=None, validation_alias=AliasChoices("sale_id", "Sale_id"))
    product_id: int | None = Field(default=None, validation_alias=AliasChoices("product_id", "Product_id"))
    quantity: int | None = None
    item_price: Decimal | None = None

    model_config = ConfigDict(populate_by_name=True)


class SaleItemRead(SaleItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
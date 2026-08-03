from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    category_name: str
    tax_rate: Decimal


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: str | None = None
    tax_rate: Decimal | None = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

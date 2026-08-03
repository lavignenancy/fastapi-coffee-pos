from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class SaleBase(BaseModel):
    timestamp: datetime
    total_amount: Decimal
    user_id: int
    customer_id: int | None = None


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    timestamp: datetime | None = None
    total_amount: Decimal | None = None
    user_id: int | None = None
    customer_id: int | None = None


class SaleRead(SaleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
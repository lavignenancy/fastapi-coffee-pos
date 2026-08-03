from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    sale_id: int
    payment_method: str
    amount_paid: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    sale_id: int | None = None
    payment_method: str | None = None
    amount_paid: Decimal | None = None


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

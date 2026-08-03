from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReceiptBase(BaseModel):
    Sale_id: int
    receipt_number: str


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    Sale_id: int | None = None
    receipt_number: str | None = None


class ReceiptRead(ReceiptBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

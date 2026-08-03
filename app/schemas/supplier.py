from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):
    supplier_name: str
    contact_name: str | None = None
    phone: str


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_name: str | None = None
    contact_name: str | None = None
    phone: str | None = None


class SupplierRead(SupplierBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

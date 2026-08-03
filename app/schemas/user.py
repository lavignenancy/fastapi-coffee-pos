from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    role: str
    is_active: bool = True


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    username: str | None = None
    hashed_password: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

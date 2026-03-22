from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "user"

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
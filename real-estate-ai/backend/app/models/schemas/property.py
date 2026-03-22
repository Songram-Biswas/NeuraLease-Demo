from pydantic import BaseModel
from typing import Optional

class PropertyRead(BaseModel):
    id: str
    title: str
    location: str
    price: float
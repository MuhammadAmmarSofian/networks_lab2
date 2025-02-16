from pydantic import BaseModel
from typing import Optional

class MenuItem(BaseModel):
    item_id: str
    name: str
    price: float
    category: Optional[str] = None

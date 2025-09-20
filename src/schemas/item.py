### src/schemas/item.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    is_available: bool = True
    order_position: int = 0

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    order_position: Optional[int] = None

class Item(ItemBase):
    id: int
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Menu schemas for public API
class MenuItemPublic(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    is_available: bool
    order_position: int
    
    class Config:
        from_attributes = True
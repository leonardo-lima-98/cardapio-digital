### src/schemas/category.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .item import Item, MenuItemPublic

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_position: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order_position: Optional[int] = None

class Category(CategoryBase):
    id: int
    restaurant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CategoryWithItems(Category):
    items: List[Item] = []

# Menu schemas for public API
class MenuCategoryPublic(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    order_position: int
    items: List[MenuItemPublic] = []
    
    class Config:
        from_attributes = True
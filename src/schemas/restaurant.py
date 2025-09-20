### src/schemas/restaurant.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .category import CategoryWithItems, MenuCategoryPublic

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

class RestaurantSummary(RestaurantBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Restaurant(RestaurantSummary):
    updated_at: Optional[datetime] = None
    categories: List[CategoryWithItems] = []

# Menu schemas for public API
class MenuPublic(BaseModel):
    restaurant: RestaurantSummary
    categories: List[MenuCategoryPublic] = []

# Resolver referências circulares
from .user import UserWithRestaurants
UserWithRestaurants.model_rebuild()
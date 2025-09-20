# src/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .restaurant import RestaurantSummary

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserWithRestaurants(User):
    restaurants: List["RestaurantSummary"] = []
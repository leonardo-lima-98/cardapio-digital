## 8. Routes Admin - Restaurantes (src/routes/admin/restaurants.py)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.models.restaurant import Restaurant
from src.schemas.restaurant import RestaurantCreate, RestaurantUpdate, Restaurant as RestaurantSchema, RestaurantSummary

router = APIRouter()

@router.post("/", response_model=RestaurantSchema)
def create_restaurant(
    restaurant: RestaurantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_restaurant = Restaurant(
        **restaurant.dict(),
        owner_id=current_user.id
    )
    
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant

@router.get("/", response_model=List[RestaurantSummary])
def list_restaurants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurants = db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantSchema)
def get_restaurant(
    restaurant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantSchema)
def update_restaurant(
    restaurant_id: str,
    restaurant_update: RestaurantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    update_data = restaurant_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
    
    db.commit()
    db.refresh(restaurant)
    
    return restaurant

@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    db.delete(restaurant)
    db.commit()
    
    return {"message": "Restaurant deleted successfully"}

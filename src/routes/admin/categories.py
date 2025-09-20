## 9. Routes Admin - Categorias (src/routes/admin/categories.py)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.models.restaurant import Restaurant
from src.models.category import Category
from src.schemas.category import CategoryCreate, CategoryUpdate, Category as CategorySchema

router = APIRouter()

def verify_restaurant_ownership(restaurant_id: str, current_user: User, db: Session):
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

@router.post("/restaurants/{restaurant_id}/categories", response_model=CategorySchema)
def create_category(
    restaurant_id: str,
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_restaurant_ownership(restaurant_id, current_user, db)
    
    db_category = Category(
        **category.dict(),
        restaurant_id=restaurant_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.get("/restaurants/{restaurant_id}/categories", response_model=List[CategorySchema])
def list_categories(
    restaurant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_restaurant_ownership(restaurant_id, current_user, db)
    
    categories = db.query(Category).filter(
        Category.restaurant_id == restaurant_id
    ).order_by(Category.order_position).all()
    
    return categories

@router.get("/categories/{category_id}", response_model=CategorySchema)
def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).join(Restaurant).filter(
        Category.id == category_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category

@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).join(Restaurant).filter(
        Category.id == category_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).join(Restaurant).filter(
        Category.id == category_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}

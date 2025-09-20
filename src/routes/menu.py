## 11. Route Pública do Menu (src/routes/menu.py)

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, selectinload
from src.core.database import get_db
from src.models.restaurant import Restaurant
from src.models.category import Category
from src.schemas.restaurant import MenuPublic

router = APIRouter()

@router.get("/", response_model=MenuPublic)
def get_menu(
    id: str = Query(..., description="Restaurant UUID"),
    db: Session = Depends(get_db)
):
    # Query restaurant with all related data
    restaurant = db.query(Restaurant)\
        .options(
            selectinload(Restaurant.categories)
            .selectinload(Category.items)
        )\
        .filter(Restaurant.id == id)\
        .first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    # Order categories and items
    ordered_categories = []
    for category in sorted(restaurant.categories, key=lambda x: x.order_position):
        ordered_items = sorted(
            [item for item in category.items if item.is_available],
            key=lambda x: x.order_position
        )
        category_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "order_position": category.order_position,
            "items": ordered_items
        }
        ordered_categories.append(category_data)
    
    return {
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "description": restaurant.description,
            "created_at": restaurant.created_at
        },
        "categories": ordered_categories
    }

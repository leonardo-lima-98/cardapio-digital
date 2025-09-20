## 10. Routes Admin - Itens (src/routes/admin/items.py)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.models.restaurant import Restaurant
from src.models.category import Category
from src.models.item import Item
from src.schemas.item import ItemCreate, ItemUpdate, Item as ItemSchema

router = APIRouter()

def verify_category_ownership(category_id: int, current_user: User, db: Session):
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

@router.post("/categories/{category_id}/items", response_model=ItemSchema)
def create_item(
    category_id: int,
    item: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_category_ownership(category_id, current_user, db)
    
    db_item = Item(
        **item.dict(),
        category_id=category_id
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.get("/categories/{category_id}/items", response_model=List[ItemSchema])
def list_items(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_category_ownership(category_id, current_user, db)
    
    items = db.query(Item).filter(
        Item.category_id == category_id
    ).order_by(Item.order_position).all()
    
    return items

@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).join(Category).join(Restaurant).filter(
        Item.id == item_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return item

@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).join(Category).join(Restaurant).filter(
        Item.id == item_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).join(Category).join(Restaurant).filter(
        Item.id == item_id,
        Restaurant.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully"}

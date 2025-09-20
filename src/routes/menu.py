## 11. Route Pública do Menu (src/routes/menu.py)

from src.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session, selectinload
from src.core.database import get_db
from src.models.restaurant import Restaurant
from src.models.category import Category
from src.schemas.restaurant import MenuPublic
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def _get_menu_data(id: str, db: Session):
    """Função auxiliar para obter dados do menu"""
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
        
        # Converter itens para dict para o template
        items_data = []
        for item in ordered_items:
            items_data.append({
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": float(item.price),  # Converter Decimal para float
                "image_url": item.image_url,
                "is_available": item.is_available,
                "order_position": item.order_position
            })
        
        category_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "order_position": category.order_position,
            "items": items_data
        }
        ordered_categories.append(category_data)
    
    return {
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone": restaurant.phone,
            "description": restaurant.description,
            "created_at": str(restaurant.created_at)
        },
        "categories": ordered_categories
    }


@router.get("/", response_class=HTMLResponse)
def get_menu_html(
    request: Request,
    id: str = Query(..., description="Restaurant UUID"),
    db: Session = Depends(get_db)
):
    """Retorna o menu em formato HTML"""
    if settings.DEBUG:
        return JSONResponse(content=_get_menu_data(id, db))
    else:
        try:
            data = _get_menu_data(id, db)

            return templates.TemplateResponse("menu.html", {
                "request": request,
                "restaurant_id": id,
                "data": data
            })
            
        except HTTPException:
            return templates.TemplateResponse("menu_not_found.html", {
                "request": request,
                "restaurant_id": id
            })

### scripts/init_db.py
#!/usr/bin/env python3
"""
Script to initialize the database with sample data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.database import SessionLocal, engine, Base
from src.models.user import User
from src.models.restaurant import Restaurant
from src.models.category import Category
from src.models.item import Item
from src.core.security import get_password_hash
from decimal import Decimal

def create_sample_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample user
        user = User(
            name="Admin User",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create sample restaurant
        restaurant = Restaurant(
            name="Restaurante Exemplo",
            address="Rua das Flores, 123, Centro",
            phone="(48) 99999-9999",
            description="Um restaurante incrível com comida deliciosa!",
            owner_id=user.id
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        
        # Create sample categories
        categories_data = [
            {"name": "Sanduíches", "description": "Nossos deliciosos sanduíches", "order_position": 1},
            {"name": "Bebidas", "description": "Bebidas refrescantes", "order_position": 2},
            {"name": "Sobremesas", "description": "Doces irresistíveis", "order_position": 3},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(
                **cat_data,
                restaurant_id=restaurant.id
            )
            db.add(category)
            categories.append(category)
        
        db.commit()
        
        # Create sample items
        items_data = [
            # Sanduíches
            {
                "name": "X-Burguer",
                "description": "Pão, hambúrguer, queijo, alface, tomate",
                "price": Decimal("15.90"),
                "category_id": categories[0].id,
                "order_position": 1
            },
            {
                "name": "X-Bacon",
                "description": "Pão, hambúrguer, queijo, bacon, alface, tomate",
                "price": Decimal("18.90"),
                "category_id": categories[0].id,
                "order_position": 2
            },
            # Bebidas
            {
                "name": "Coca-Cola 350ml",
                "description": "Refrigerante gelado",
                "price": Decimal("5.00"),
                "category_id": categories[1].id,
                "order_position": 1
            },
            {
                "name": "Suco de Laranja",
                "description": "Suco natural de laranja",
                "price": Decimal("6.50"),
                "category_id": categories[1].id,
                "order_position": 2
            },
            # Sobremesas
            {
                "name": "Pudim",
                "description": "Pudim caseiro com calda de caramelo",
                "price": Decimal("8.00"),
                "category_id": categories[2].id,
                "order_position": 1
            }
        ]
        
        for item_data in items_data:
            item = Item(**item_data)
            db.add(item)
        
        db.commit()
        
        print(f"✅ Sample data created successfully!")
        print(f"📍 Restaurant ID: {restaurant.id}")
        print(f"👤 Admin User: admin@example.com / admin123")
        print(f"🌐 Menu URL: http://localhost:8000/menu/?id={restaurant.id}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()

### src/models/category.py
import uuid
from sqlalchemy import String as SQLString
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(SQLString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    order_position = Column(Integer, default=0)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="categories")
    items = relationship("Item", back_populates="category", cascade="all, delete-orphan")
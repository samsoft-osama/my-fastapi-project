"""
Menu item model for food menu management
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class MenuItem(Base):
    """Menu item model for food menu management"""
    
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="menu_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price})>"
    
    @property
    def formatted_price(self) -> str:
        """Get formatted price string"""
        return f"${self.price:.2f}" 
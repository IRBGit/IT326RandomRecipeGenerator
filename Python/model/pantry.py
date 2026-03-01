from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from model.base import Base


class PantryItem(Base):
    __tablename__ = "pantry_items"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)

    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # Relationships
    user = relationship("User", back_populates="pantry_items")
    ingredient = relationship("Ingredient", back_populates="pantry_items")

    def __repr__(self):
        return f"<PantryItem(user_id={self.user_id}, ingredient_id={self.ingredient_id}, quantity={self.quantity}, unit='{self.unit}')>"
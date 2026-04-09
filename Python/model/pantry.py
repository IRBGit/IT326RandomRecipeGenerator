"""
    Authors: Jon Bailey and 
"""
from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from model.base import Base
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from model import User, Ingredient


class PantryItem(Base):
    __tablename__ = "pantry_items"

    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("ingredients.id"), 
        primary_key=True)

    quantity: Mapped[Optional[float]] = mapped_column(
        Float, 
        nullable = True)
    unit: Mapped[Optional[str]] = mapped_column(
        String(50), 
        nullable = True)

    # Relationships
    user: Mapped["User"] = relationship("User", 
                        back_populates="_pantry")
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", 
        back_populates="pantry_items")

    def __init__(
            self, 
            ingredient: "Ingredient",
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
            ):
        if quantity is not None and quantity <= 0:
            raise ValueError("Quantity may not be less than 0")
        if unit is not None and quantity is None:
            raise ValueError("Unit may not exist without a quantity.")

        self.quantity = quantity
        self.unit = unit
        self.ingredient = ingredient

    def __repr__(self):
        return f"<PantryItem(user_id={self.user_id}, ingredient_id={self.ingredient_id}, quantity={self.quantity}, unit='{self.unit}')>"
    
    def __eq__(self, other: PantryItem) -> bool:
        if not isinstance(other, PantryItem):
            return False
        from model import User, Ingredient
        if self.ingredient_id == other.ingredient_id and self.user_id == other.user_id:
            return True
        elif self.user.id == other.user.id and self.ingredient_id == other.ingredient_id:
            return True
        elif self.ingredient.id == other.ingredient.id and self.user_id == other.user_id:
            return True
        elif self.ingredient.id == other.ingredient.id and self.user.id == other.user.id:
            return True
        else:
            return False
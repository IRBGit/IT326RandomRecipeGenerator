"""
    Authors: Jon Bailey and 
"""
from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from model.base import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from model import User, Ingredient


class PantryItem(Base):
    __tablename__ = "pantry_items"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"), primary_key=True)

    quantity: Mapped[float] = mapped_column(Float, nullable = True)
    unit: Mapped[str] = mapped_column(String(50), nullable = True)

    # Relationships
    user: Mapped["User"] = relationship("User", 
                        back_populates="pantry_items")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", 
                              back_populates="pantry_items")

    def __repr__(self):
        return f"<PantryItem(user_id={self.user_id}, ingredient_id={self.ingredient_id}, quantity={self.quantity}, unit='{self.unit}')>"
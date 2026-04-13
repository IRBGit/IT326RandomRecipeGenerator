from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from model.base import Base
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from model import Recipe, Ingredient

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"), primary_key=True)

    quantity: Mapped[float] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relationships
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="_ingredients")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="recipe_associations")

    def __init__(self, quantity: float = 0.0, unit: str = "", ingredient: Optional[Ingredient] = None):
        self.quantity = quantity
        self.unit = unit
        if ingredient:
            self.ingredient = ingredient
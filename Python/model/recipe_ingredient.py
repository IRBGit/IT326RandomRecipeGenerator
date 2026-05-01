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

    quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    recipe: Mapped["Recipe"] = relationship(
        "Recipe", 
        back_populates = "_ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", 
        back_populates = "recipe_association")

    def __init__(
            self, 
            ingredient: "Ingredient",
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
        ):
        if ingredient is None:
            raise ValueError("ingredient cannot be None")
        
        # Rule 1: quantity must be > 0 if provided.
        if quantity is not None and quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        
        # Rule 2: unit requires quantity
        if unit is not None and quantity is None:
            raise ValueError("unit cannot be set without a quantity")

        self.quantity = quantity
        self.unit = unit
        self.ingredient = ingredient

    def __eq__(
            self, 
            other: object
            ) -> bool:
        if not isinstance(other, RecipeIngredient):
            return False
        from model import Ingredient, Recipe
        return self.ingredient == other.ingredient and self.recipe == other.recipe
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.id))
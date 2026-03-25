"""
    Authors: Jon Bailey and Thaanvi Ambala
"""

from __future__ import annotations
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Sequence
from model.base import Base
from model.associations import recipe_ingredients
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from model import Recipe, PantryItem

# This class is for the backend of ingredients

#TODO: include methods for the different Use Cases, acording to Class Diagram
#TODO: Add setters/getters


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, Sequence("ingredient_id_seq"), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Recipes that use this ingredient
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary=recipe_ingredients,
        back_populates="ingredients"
    )

    pantry_items: Mapped[List[PantryItem]] = relationship(
    "PantryItem",
    back_populates="ingredient"
)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"

    def get_name(self) -> str:
        assert isinstance(self.name, str)
        return self.name

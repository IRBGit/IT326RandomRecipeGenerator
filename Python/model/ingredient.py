"""
    Authors: Jon Bailey and Thaanvi Ambala
"""

from __future__ import annotations
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Sequence
from model.base import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from model import Recipe, PantryItem, RecipeIngredient

# This class is for the backend of ingredients

#TODO: include methods for the different Use Cases, acording to Class Diagram
#TODO: Add setters/getters


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(
        Integer, 
        Sequence("ingredient_id_seq"), 
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        unique=True
        )

    # Recipes that use this ingredient
    recipe_association: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="ingredient",
        cascade = "all, delete-orphan"
        )

    pantry_items: Mapped[List["PantryItem"]] = relationship(
    "PantryItem",
    back_populates="ingredient",
    cascade = "all, delete-orphan"
        )

    def __init__(
            self, 
            name: str
            ):
        self.name = name

    def __repr__(
            self
            ):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"

    def get_name(
            self
            ) -> str:
        assert isinstance(self.name, str)
        return self.name
    
    def __eq__(
            self, 
            other: object
            ) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.id is not None and other.id is not None and self.id == other.id
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.id))
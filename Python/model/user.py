"""
    Author: Jon Bailey and Thanvi Ambala
"""

from __future__ import annotations

# models.py (continuing from Recipe)
from __future__ import annotations # delays type checking to prevent runtime errors.
from typing import Optional, TYPE_CHECKING, Any, List

from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import relationship, Mapped, mapped_column
from model.base import Base
from model.associations import user_favorites
from model.pw_hash import PWHash

if TYPE_CHECKING:
    from model import Ingredient, PantryItem, Recipe, Rating


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, 
                Sequence('user_id_seq'),
                primary_key=True)
    email: Mapped[str] = mapped_column(String(255), 
                   unique=True, 
                   nullable=False)
    password: Mapped[str] = mapped_column(String(255), 
                      nullable=False)

    # Many-to-many relationship to Recipe
    favorites: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary=user_favorites,
        back_populates="favorited_by"
    )

    ratings: Mapped[List["Rating"]] = relationship(
        "Rating", 
        back_populates = "user", 
        cascade = "all, delete-orphan"
        )

    pantry_items: Mapped[List["PantryItem"]] = relationship(
        "PantryItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = PWHash().hashPassword(password)
        

    def check_password(self, toCheck: str) -> bool:
        return PWHash().verify(self.password, toCheck)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
    
    
    """Proposed location for add_ingredient_to_pantry() and 
    remove_ingredient_from_pantry() methods."""

    # annotations from __future__ allows type checking at run time.
    def add_ingredient_to_pantry(
            self, 
            ingredient: Ingredient, 
            quantity: Optional[int] = None, 
            unit: Optional[str] = None
            )-> PantryItem:
        """
        Add a new ingredient to the pantry or update the existing item.

        Args:
            ingredient(Ingredient): The ORM Ingredient model
            quantity(int): The number of units of the ingredient
            unit(str): The units of the ingredient (kg, lb, inches, meters, etc.)

        Returns:
            item(PantryItem): The PantryItem is returned to the user.
        """
        from model import PantryItem, Ingredient

        for item in self.pantry_items:
            if item.ingredient == ingredient:
                if quantity is not None:
                    item.quantity = quantity
                if unit is not None:
                    item.unit = unit
                return item
                
        pantry_item = PantryItem(
            user = self,
            ingredient = ingredient,
            quantity = quantity,
            unit = unit
        )
        self.pantry_items.append(pantry_item)
        return pantry_item
    
    # annotations from __future__ allows type checking at run time.
    def remove_ingredient_from_pantry(
            self, 
            ingredient: Ingredient
            ) -> PantryItem | None:
        """
        Remove an ingredient from the user's pantry.
        """
        from model import PantryItem

        for item in self.pantry_items:
            if item.ingredient == ingredient:
                self.pantry_items.remove(item)
                return item
        return None
    
    def update_pantry_item(
            self, 
            ingredient: Ingredient, 
            quantity: Optional[int] = None, 
            unit: Optional[str] = None
            ) -> PantryItem | None:
        """
        Update the quantity or unit for an ingredient in the user's pantry.
        """
        from model import PantryItem

        for item in self.pantry_items:
            if item.ingredient == ingredient:
                if quantity is not None:
                    item.quantity = quantity
                if unit is not None:
                    item.unit = unit
                return item
        return None
    
    def get_pantry(self) -> list[dict[str, Any]] | None:
        """
        Returns the items in the user's pantry.

        Returns:
            items(Ingredients): A list of ingredients in the pantry.
        """
        return [
            {
                "ingredient": item.ingredient.name,
                "quantity": item.quantity,
                "unit": item.unit
            }
            for item in self.pantry_items
        ]
    
    def get_id(self) -> int:
        return self.id
    
    def delete_account(self):
        print("Deleting user account...")

    def reset_password(self, new_password: str):
        self.password = PWHash().hashPassword(new_password)
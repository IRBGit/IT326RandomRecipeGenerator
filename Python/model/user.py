"""
    Author: Jon Bailey and Thanvi Ambala
"""

from __future__ import annotations

# models.py (continuing from Recipe)
from __future__ import annotations # delays type checking to prevent runtime errors.
from typing import Optional, TYPE_CHECKING, Any, List

from sqlalchemy import Integer, String, Sequence
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from model.base import Base
from model.associations import user_favorites
from model.pw_hash import PWHash

if TYPE_CHECKING:
    from model import Ingredient, PantryItem, Recipe, Rating, UserRecipeNote


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

    _ratings: Mapped[dict["Recipe", "Rating"]] = relationship(
        "Rating", 
        collection_class = attribute_mapped_collection("recipe"),
        back_populates = "user", 
        cascade = "all, delete-orphan"
        )
    
    """This cannot be set from the User side. Must be set by methods in the Recipe class."""
    recipe_rating: AssociationProxy[dict["Recipe", int]] = association_proxy(
        "_rating",
        "rating"
    )

    pantry: AssociationProxy[dict["Ingredient", "PantryItem"]] = association_proxy(
        "_pantry",
        "self",
        creator = lambda i, p: p # 'i' is the ingredient key, and 'p' is the PantryItem value
    )

    _pantry: Mapped[List["PantryItem"]] = relationship(
        "PantryItem",
        collection_class = attribute_mapped_collection("ingredient"),
        back_populates="user",
        cascade="all, delete-orphan"
    )

    _recipe_notes: Mapped[dict["Recipe", "UserRecipeNote"]] = relationship(
        "UserRecipeNote",
        collection_class = attribute_mapped_collection("recipe"),
        back_populates = "user",
        cascade = "all, delete-orphan"
    )

    notes: AssociationProxy[dict["Recipe", list[str]]] = association_proxy(
        "_recipe_notes",
        "notes",
        creator = lambda r, n: UserRecipeNote(recipe = r, notes = n)
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
            quantity: Optional[float] = None, 
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

        # 1. Check if it already exists in our Map
        if ingredient in self.pantry:
            item = self.pantry[ingredient]
            if quantity is not None:
                item.quantity = quantity
            if unit is not None:
                item.unit = unit
            return item
        
        # 2. If it doesn't exist, use the Map to add it
        # The 'user' is handled automatically because we are adding to self.pantry
        new_item = PantryItem(quantity=quantity or 0.0, unit=unit or "")
        self.pantry[ingredient] = new_item
        return new_item
    
    # annotations from __future__ allows type checking at run time.
    def remove_ingredient_from_pantry(
            self, 
            ingredient: Ingredient
            ) -> PantryItem | None:
        """
        Remove an ingredient from the user's pantry.
        """
        from model import PantryItem

        return self.pantry.pop(ingredient, None)
    
    def update_pantry_item(
            self, 
            ingredient: Ingredient, 
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
            ) -> PantryItem | None:
        """
        Update the quantity or unit for an ingredient in the user's pantry.
        """
        from model import PantryItem

        item = self.pantry.get(ingredient)
        if item:
            item.quantity = quantity
            item.unit = unit
        return item
    
    def get_pantry(self) -> list[dict[str, Any]] | None:
        """
        Returns the items in the user's pantry.

        Returns:
            items(Ingredients): A list of ingredients in the pantry.
        """
        return [
            {
                "ingredient": ing.name,
                "quantity": item.quantity,
                "unit": item.unit
            }
            for ing, item in self.pantry_items
            ]
    
    def get_id(self) -> int:
        return self.id
    
    def delete_account(self):
        print("Deleting user account...")

    def reset_password(self, new_password: str):
        self.password = PWHash().hashPassword(new_password)
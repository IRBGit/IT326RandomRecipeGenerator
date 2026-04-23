"""
    Author: Jon Bailey
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

    id: Mapped[int] = mapped_column(
        Integer, 
        Sequence('user_id_seq'),
        primary_key=True
        )
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        nullable=False
        )
    password: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
        )

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
        "_ratings",
        "rating"
        )

    pantry: AssociationProxy[
        dict[
            "Ingredient", 
            "PantryItem"
            ]
        ] = association_proxy(
        "_pantry",
        "self",
        creator = lambda i, p: p # 'i' is the ingredient key, and 'p' is the PantryItem value
    )

    _pantry: Mapped[dict[int, "PantryItem"]] = relationship(
        "PantryItem",
        collection_class = attribute_mapped_collection(
            "ingredient_id"
            ),
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
        return PWHash().verify(hash = self.password, password = toCheck)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
    
    
    """Proposed location for add_ingredient_to_pantry() and 
    remove_ingredient_from_pantry() methods."""

    # annotations from __future__ allows type checking at run time.
    def add_ingredient_to_pantry(
            self, 
            ingredient: "Ingredient", 
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
            )-> "PantryItem":
        """
        Add a new ingredient to the pantry or update the existing item.

        Args:
            ingredient(Ingredient): The ORM Ingredient model
            quantity(int): The number of units of the ingredient
            unit(str): The units of the ingredient (kg, lb, inches, meters, etc.)

        Returns:
            item(PantryItem): The PantryItem is returned to the user.
        """
        from model import PantryItem

        if ingredient.id is None:
            raise ValueError("Ingredient must be persisted (have an id)")
        
        key = ingredient.id

        if key in self._pantry:
            item = self._pantry[key]

            if quantity is not None:
                item.quantity = quantity
            if unit is not None:
                item.unit = unit

            return item
        
        # 2. If it doesn't exist, use the Map to add it
        # The 'user' is handled automatically because we are adding to self.pantry
        if quantity is not None and quantity <= 0:
            raise ValueError("Qauntity must be greater than 0.")
        if unit is not None and quantity is None:
            raise ValueError("You cannot have a unit without a quantity")
        
        if quantity is None and unit is None:
            new_item = PantryItem(ingredient = ingredient)
        elif unit is None:
            new_item = PantryItem(ingredient = ingredient, quantity = quantity)
        else: 
            new_item = PantryItem(quantity=quantity, unit=unit, ingredient = ingredient)
        self._pantry[key] = new_item
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

        if ingredient.id is None:
            raise ValueError("Ingredient must have an id")
        
        key = ingredient.id

        return self._pantry.pop(key, None)
    
    def update_pantry_item(
            self, 
            ingredient: "Ingredient", 
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
            ) -> "PantryItem | None":
        """
        Update the quantity or unit for an ingredient in the user's pantry.
        """
        from model import PantryItem

        if ingredient.id is None:
            raise ValueError("Ingredient must have an id")
        
        key = ingredient.id
        item = self._pantry.get(key)
        if item:
            if quantity is not None and quantity <= 0:
                raise ValueError("Quantity may not be less than or equal to 0.")
            if unit is not None and quantity is None:
                raise ValueError("Unit may not exist without a quantity.")
            
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
                "ingredient_id": item.ingredient.id,
                "ingredient": item.ingredient.name,
                "quantity": item.quantity,
                "unit": item.unit
            }
            for ing, item in self._pantry_items
            ]
    
    def get_id(self) -> int:
        return self.id
    
    def __eq__(
            self, 
            other: object
            ) -> bool:
        if not isinstance(other, User):
            return False
        return self.id is not None and other.id is not None and self.id == other.id
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.id))
    
    def add_note(
            self, 
            recipe: "Recipe", 
            note: str
        ) -> list[str]:
        if recipe in self.notes:
            notes = self.notes[recipe]
            notes.append(note)
            self.notes[recipe] = notes
        else:
            self.notes[recipe] = [note]

        return self.notes[recipe]
    
    def remove_note(
            self, recipe: "Recipe",
            note: str
    ) -> list[str]:
        """
        Remove a specific note for a given recipe.

        Returns:
            Updated list of notes.
        """
        if recipe not in self.notes:
            raise KeyError("No notes found for this recipe")
        
        notes_list = self.notes[recipe]

        if note not in notes_list:
            raise ValueError("Note not found")
        
        notes_list.remove(note)

        self.notes[recipe] = notes_list

        return notes_list
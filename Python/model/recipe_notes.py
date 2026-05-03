from __future__ import annotations
import json
from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from model import User, Recipe

class UserRecipeNote(Base):
    __tablename__ = "user_recipe_notes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        primary_key = True
        )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"), 
        primary_key = True
        )
    
    # The raw string stored in the DB (lines separated by \n)
    _notes_raw: Mapped[str] = mapped_column(
        "notes", 
        Text, 
        default = ""
        )

    # Relationships
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "_recipe_notes"
        )
    recipe: Mapped["Recipe"] = relationship(
        "Recipe", 
        back_populates = "_user_notes"
        )

    # Python-side List Interface
    @property
    def notes(
        self
        ) -> list[str]:
        """
        Getter method for notes.

        Returns:
            A list of strings.
        """
        if not self._notes_raw:
            return []
        return self._notes_raw.split("\n")

    @notes.setter
    def notes(
        self, 
        value: list[str]
        ):
        """
        Setter method for notes, converts a list of strings into a single string for storage into a single text block. 
        Each string in the note will be seperated by '\\n' before storage
        

        """

        self._notes_raw = "\n".join(value) if value else ""

    def __repr__(
            self
            ):
        return f"<UserRecipeNote(user_id={self.user_id}, recipe_id={self.recipe_id})>"
    
    def __eq__(
            self,
            other: object
    ) -> bool:
        if not isinstance(other, UserRecipeNote):
            return False
        from model import User, Recipe
        return (
            self.recipe_id is not None and
            self.user_id is not None and
            self.recipe_id == other.recipe_id and 
            self.user_id == other.user_id
        )
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.user_id, self.recipe_id))

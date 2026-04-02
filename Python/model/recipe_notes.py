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

    def __init__(
            self, 
            notes: Optional[list[str]] = None, 
            **kwargs
            ):
        super().__init__(**kwargs)
        self.notes = notes or []

    # Python-side List Interface
    @property
    def notes(
        self
        ) -> list[str]:
        if not self._notes_raw:
            return []
        return self._notes_raw.split("\n")

    @notes.setter
    def notes(
        self, 
        value: list[str]
        ):
        self._notes_raw = "\n".join(value) if value else ""

    def __repr__(
            self
            ):
        return f"<UserRecipeNote(user_id={self.user_id}, recipe_id={self.recipe_id})>"
from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, TYPE_CHECKING, Optional
from model.base import Base

if TYPE_CHECKING:
    from model import User, Recipe

class Rating(Base):
    __tablename__ = "ratings"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key = True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"), primary_key = True)

    rating: Mapped[int] = mapped_column(Integer, nullable = False)

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name = "check_rating_range"),
    )

    #Relationships
    user: Mapped["User"] = relationship("User", back_populates="_ratings")
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="_ratings")

    def __init__(self, user: Optional[User] = None, recipe: Optional[Recipe] = None, rating: int = 0):
        self.user = user
        self.recipe = recipe
        self.rating = rating

    def __repr__(self):
        return f"Rating(user_id = {self.user_id}, recipe_id = {self.recipe_id}, rating = {self.rating})>"
    
    def __eq__(
            self, 
            other: object
            ) -> bool:
        if not isinstance(other, Rating):
            return False
        from model import User, Recipe
        return self.user == other.user and self.recipe == other.recipe
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.id))
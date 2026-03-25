"""
    Authors: Jon Bailey and 
"""

# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Sequence, Text
from sqlalchemy.ext.hybrid import hybrid_property
from model.base import Base
from model import user_favorites, recipe_ingredients
import json
from typing import List

if TYPE_CHECKING:
    from model import Rating, User, Ingredient

class Recipe(Base):
    __tablename__ = "recipes" # Table name in the SQL database

    id: Mapped[int] = mapped_column(Integer, 
                Sequence('recipe_id_seq'),
                primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable = False)
    # area = Column() # I don't know what this is supposed to be but it can't be an empty column to write to the database.
    _instructions: Mapped[str] = mapped_column("intstructions", Text, nullable=False)
    

    # This relationship is automatically created via the backref in User and explicitly identified here.
    favorited_by: Mapped[List["User"]] = relationship(
        "User", 
        secondary = user_favorites, 
        back_populates = "favorites")

    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient",
        secondary=recipe_ingredients,
        back_populates="recipes"
    )

    ratings: Mapped[List["Rating"]] = relationship(
        "Rating",
        back_populates = "recipe",
        cascade = "all, delete-orphan"
    )

    # def __init__(self, name: str, instructions: list[str] | None = None):
    #     self.name = name
    #     self.instructions = instructions or []

    # init includes name, category, instructions, tags, and video as setters
    def __init__(self, name: str, ingredients: str = None, instructions: str = None, category: str = None, tags = None, video: str = None):
        self.name = name # in database
        self.category = None 
        self.area = None
        self.ingredients = ingredients or [] # for now, including all variables, change later
        # ingredients in database
        self.instructions = instructions # in database
        self.category = category
        self.tags = tags
        self.video = video

    def __repr__(self):
        return f"<Recipe(id = {self.id}, name ='{self.name}')>"
    
    # prints a recipe to terminal
    def print(self):
        print(self.name)
        if (self.category):
            print(self.category)

        if (self.area):
            print(self.area)

        if (self.ingredients):
            print(self.ingredients)

        if (self.instructions):
            print(self.instructions)

        if (self.category):
            print(self.category)
            
        if (self.tags):
            print(self.tags)

        if (self.video):
            print(self.video)
    @property
    def instructions(self) -> list[str]:
        # This is what you'll use in your Python code: recipe.instructions
        try:
            return json.loads(self._instructions)
        except (json.JSONDecodeError, TypeError):
            return []

    @instructions.setter
    def instructions(self, value: list[str]):
        self._instructions = json.dumps(value or [])

    def get_average_rating(self) -> float:
        from model import Rating
        if not self.ratings:
            return 0.0
        return sum(r.rating for r in self.ratings) / len(self.ratings)

    def get_user_rating(self, user) -> int | None:
        from model import Rating
        for r in self.ratings:
            if r.user == user:
                return r.rating
        return None
    
    def add_rating(self, user: User, value: int) -> Rating:
        from model import Rating
        if value < 0 or value > 5:
            raise ValueError("rating must be between 0 and 5")
        
        for r in self.ratings:
            if r.user == user:
                r.rating = value
                return r
        
        rating = Rating(user = user, recipe = self, rating = value)
        self.ratings.append(rating)
        return rating
    
    def get_name(self) -> str:
        return self.name

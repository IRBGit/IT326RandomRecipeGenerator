"""
    Authors: Jon Bailey and 
"""

# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Column, Sequence, Text
from model.base import Base
from model.associations import user_favorites, recipe_ingredients
import json

class Recipe(Base):
    __tablename__ = "recipes" # Table name in the SQL database

    id = Column(Integer, 
                Sequence('recipe_id_seq'),
                primary_key=True)
    name = Column(String(255), nullable = False)
    # area = Column() # I don't know what this is supposed to be but it can't be an empty column to write to the database.
    instructions = Column(Text, nullable=False)
    

    # This relationship is automatically created via the backref in User and explicitly identified here.
    favorited_by = relationship(
        "User", 
        secondary = user_favorites, 
        back_populates = "favorites")

    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredients,
        back_populates="recipes"
    )

    ratings = relationship(
        "Rating",
        back_populates = "recipe",
        cascade = "all, delete-orphan"
    )

    def __init__(self, name: str, instructions: list[str]= []):
        self.name = name
        self.instructions = json.dumps(instructions or [])

    def __repr__(self):
        return f"<Recipe(id = {self.id}, name ='{self.name}')>"
    
    @property
    def instructions_list(self):
        return json.loads(self.instructions) #type: ignore
    
    @instructions_list.setter
    def instructions_list(self, value):
        self.instructions = json.dumps(value)

    def get_average_rating(self) -> float:
        if not self.ratings:
            return 0.0
        return sum(r.rating for r in self.ratings) / len(self.ratings)

    def get_user_rating(self, user) -> int | None:
        for r in self.ratings:
            if r.user == user:
                return r.rating
        return None
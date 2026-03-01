# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Table, Column, ForeignKey
from model.base import Base
from model.associations import user_favorites, recipe_ingredients

recipe_ingredients = Table(
    "recipe_ingredients", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
    
)

class Recipe(Base):
    __tablename__ = "recipe" # Table name in the SQL database

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    def __init__(self, name: str, instructions: str = None):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"<Recipe(id = {self.id}, name ='{self.name}')>"
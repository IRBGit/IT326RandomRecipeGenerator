# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Column, Sequence
from model.base import Base
from model.associations import user_favorites, recipe_ingredients

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

    # init includes name, category, instructions, tags, and video as setters
    def __init__(self, name: str, instructions: str = None, category: str = None, tags = None, video: str = None):
        self.name = name
        self.category = None
        self.area = None
        self.ingredients = None # for now, including all variables, change later
        self.instructions = instructions
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
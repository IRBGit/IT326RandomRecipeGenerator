# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Table, Column, ForeignKey, List


Base = declarative_base()

recipe_ingredients = Table(
    "recipe_ingredients", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipe.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True)
    
)

class Recipe(Base):
    __tablename__ = "recipe" # Table name in the SQL database

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable = False)
    category = Column(String)
    area = Column(String)
    ingredients = relationship("ingredient", backref="Recipe")
    instructions = Column(String, nullable=False)
    tags = Column(String)
    video = Column(String)


    

    # This relationship is automatically created via the backref in User and explicitly identified here.
    favorited_by = relationship("User", secondary = "user_favorites", back_populates = "favorites")

    def __init__(self, name: str, instructions: str = None):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"<Recipe(id = {self.id}, name ='{self.name}')>"
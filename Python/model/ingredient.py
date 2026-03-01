from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from model.base import Base
from model.associations import recipe_ingredients

# This class is for the backend of ingredients

#TODO: include methods for the different Use Cases, acording to Class Diagram
#TODO: Add setters/getters



class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    # Recipes that use this ingredient
    recipes = relationship(
        "Recipe",
        secondary=recipe_ingredients,
        back_populates="ingredients"
    )

    pantry_items = relationship(
    "PantryItem",
    back_populates="ingredient"
)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"
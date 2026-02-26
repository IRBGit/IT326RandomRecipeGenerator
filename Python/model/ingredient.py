from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
import model.recipe

# This class is for the backend of ingredients

#TODO: include methods for the different Use Cases, acording to Class Diagram
#TODO: Add setters/getters

Base = declarative_base()

recipe_ingredients = Table(
    "recipe_ingredients", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True)
    
)

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    # Recipes that use this ingredient
    recipes = relationship(
        "Recipe",
        secondary=recipe_ingredients,
        back_populates="ingredient"
    )

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"
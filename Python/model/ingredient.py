from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)

    # A user can have many pantry items
    pantry_items = relationship(
        "PantryItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class PantryItem(Base):
    """
    One row = one ingredient saved to one user's pantry.
    You can also store quantity/unit (optional).
    """
    __tablename__ = "pantry_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    quantity = Column(String(50), nullable=True)  # e.g. "2"
    unit = Column(String(50), nullable=True)      # e.g. "cups"

    user = relationship("User", back_populates="pantry_items")
    ingredient = relationship("Ingredient", back_populates="pantry_items")

    def __repr__(self):
        return (
            f"<PantryItem(user_id={self.user_id}, ingredient_id={self.ingredient_id}, "
            f"quantity={self.quantity}, unit={self.unit})>"
        )

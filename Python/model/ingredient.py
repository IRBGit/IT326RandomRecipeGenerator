from flask import session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from model.base import Base
from model.associations import recipe_ingredients
from model import User, PantryItem

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

    def add_ingredient_to_pantry(self, session, user: User, ingredient_name: str, quantity=None, unit=None):
        """
        Saves an ingredient into the user's pantry.
        - If the ingredient doesn't exist in the ingredients table, it creates it.
        - Then it creates a PantryItem linking user <-> ingredient.
        """
        # 1) Find or create the ingredient
        ingredient = session.query(Ingredient).filter_by(name=ingredient_name).first()
        if ingredient is None:
            ingredient = Ingredient(name=ingredient_name)
            session.add(ingredient)
            session.flush()  # gives ingredient an id without committing yet

        # 2) Check if it's already in the pantry (so we don't duplicate)
        existing = (
            session.query(PantryItem)
            .filter_by(user_id=user.id, ingredient_id=ingredient.id)
            .first()
        )
        if existing:
            # If you want, update quantity/unit instead of duplicating
            existing.quantity = quantity or existing.quantity
            existing.unit = unit or existing.unit
            session.commit()
            return existing

        # 3) Add pantry item
        pantry_item = PantryItem(
            user_id=user.id,
            ingredient_id=ingredient.id,
            quantity=quantity,
            unit=unit
        )
        session.add(pantry_item)
        session.commit()
        return pantry_item


    def remove_ingredient_from_pantry(self, session, user: User, ingredient_name: str):
        """Removes an ingredient from the user's pantry (if it exists)."""
        ingredient = session.query(Ingredient).filter_by(name=ingredient_name).first()
        if ingredient is None:
            return False

        pantry_item = (
            session.query(PantryItem)
            .filter_by(user_id=user.id, ingredient_id=ingredient.id)
            .first()
        )
        if pantry_item is None:
            return False

        session.delete(pantry_item)
        session.commit()
        return True
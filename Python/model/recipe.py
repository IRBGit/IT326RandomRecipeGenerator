"""
    Authors: Jon Bailey and 
"""

# This class handles the data of Recipes

#TODO: include methods for the different Use Cases, according to Class Diagram
#TODO: Add setters/getters

from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Sequence, Text, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from model.base import Base
from model import user_favorites
import json
from typing import List
from datetime import datetime

if TYPE_CHECKING:
    from model import Rating, User, Ingredient, RecipeIngredient, UserRecipeNote

class Recipe(Base):
    __tablename__ = "recipes" # Table name in the SQL database

    id: Mapped[int] = mapped_column(Integer, 
                Sequence('recipe_id_seq'),
                primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable = False, unique=True)
    # area = Column() # I don't know what this is supposed to be but it can't be an empty column to write to the database.
    _instructions: Mapped[str] = mapped_column("intstructions", Text, nullable=False)
    # Alysa Solomon: published time should be added here, IDK how to add it
    # It should be able to store a big number, from reaserch DATETIME will probably be most helpful
    # additonally need to add quanity, still don't know how to add columns via code
    published_time: Mapped[datetime] = mapped_column("published_time", DateTime, nullable=True)

    # This relationship is automatically created via the backref in User and explicitly identified here.
    favorited_by: Mapped[List["User"]] = relationship(
        "User", 
        secondary = user_favorites, 
        back_populates = "favorites")

    _ingredients: Mapped[dict[int, "RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        collection_class = attribute_mapped_collection(
            "ingredient_id"
            ),
        back_populates="recipe",
        cascade = "all, delete-orphan"
    )

    recipe_ingredients: AssociationProxy[dict["Ingredient", "RecipeIngredient"]] = association_proxy(
        "_ingredients",
        "self",
        creator = lambda i, ri: ri
    )
    
    _ratings: Mapped[dict["User", "Rating"]] = relationship(
        "Rating",
        collection_class = attribute_mapped_collection("user"),
        back_populates = "recipe",
        cascade = "all, delete-orphan"
    )

    user_ratings: AssociationProxy[dict["User", int]] = association_proxy(
        "_ratings",
        "rating",
        creator = lambda u, v: Rating(user = u, rating = v)
    )

    _user_notes: Mapped[dict["User", "UserRecipeNote"]] = relationship(
        "UserRecipeNote",
        collection_class = attribute_mapped_collection("user"),
        back_populates = "recipe",
        cascade = "all, delete-orphan"
    )

    # def __init__(self, name: str, instructions: list[str] | None = None):
    #     self.name = name
    #     self.instructions = instructions or []

        # init includes name, category, instructions, tags, and video as setters
    def __init__(self, name: str, ingredients: Optional[List["Ingredient"]], instructions: Optional[List[str]] | None = None, pub_time: Optional[datetime] | None = None,category: Optional[str] = None, tags = None, video: Optional[str] = None):
        self.name = name
        self.category = None
        self.area = None
        # self.ingredients = ingredients or [] # for now, including all variables, change later
        self.instructions = instructions or []
        self.category = category
        self.tags = tags
        self.video = video
        self.published_time = pub_time

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
        if not self.user_ratings:
            return 0.0
        return sum(self.user_ratings.values()) / len(self.user_ratings)

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
    
    def add_ingredient(
            self, 
            ingredient: Ingredient, 
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
    ) -> "RecipeIngredient" :
        from model import RecipeIngredient

        if ingredient.id is None:
            raise ValueError("Ingredient must be presisted (have an id from the database)")
        
        key = ingredient.id

        if key in self._ingredients:
            assoc = self._ingredients[key]
            if quantity is not None and quantity <= 0:
                raise ValueError("Quantity must be greater than 0")
            if unit is not None and quantity is None:
                raise ValueError("Unit cannot be set without a quantity")
            
            assoc.unit = unit
            assoc.quantity = quantity
            return assoc
        
        assoc = RecipeIngredient(
            ingredient = ingredient,
            quantity = quantity,
            unit = unit
        )
        self._ingredients[ingredient] = assoc
        return assoc
    
    def remove_ingredient(
            self,
            ingredient: "Ingredient"
    ) -> "RecipeIngredient | None":
        """
        Remove an ingredient from the recipe.

        Returns:
            The removed RecipeIngredient or None if it wasn't present.
        """
        if ingredient.id is None:
            raise ValueError("Ingredient must have an id")
        
        key = ingredient.id

        if key not in self._ingredients:
            raise KeyError(f"{ingredient} not in recipe.")

        return self._ingredients.pop(key)
    

    def __eq__(
            self, 
            other: object
            ) -> bool:
        if not isinstance(other, Recipe):
            return False
        return self.id is not None and other.id is not None and self.id == other.id
    
    def __hash__(
            self
            ) -> int:
        return hash((type(self), self.id))
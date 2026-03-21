"""
    Author: Jon Bailey
"""

from db.db_query import DBQuery
from db.db_connect import DBConnect
from model import Ingredient, User, PantryItem, Recipe, recipe_ingredients, user_favorites
import re
from typing import Optional

class PantryService:
    """
    
    """
    def __init__(self, db_query: DBQuery):
        self.db = db_query
    
    def add_ingredient_to_pantry(
            self, 
            user: User, 
            ingredient: Ingredient, 
            quantity: Optional[int | None] = None, 
            unit: Optional[str | None] = None
            ) -> PantryItem | None:
        """
        Add an ingredient to a user's pantry.
        Creates the ingredient if it does not exist.

        Args:
            user(User): The ORM user object.
            ingredient_name(str): The ingredient name for a database search.
            quantity(int): The amount of the ingredient.
            unit(str): The type of unit for the ingredient's amount.
        
        Returns:
            Optional(PantryItem): Will return the PantryItem object if it succeeds.
        """

        # use the User domain method
        pantry_item = user.add_ingredient_to_pantry(
            ingredient,
            quantity,
            unit
        )

        self.db.commit_transaction()

        return pantry_item
    
    def remove_ingredient_from_pantry(
            self, 
            user: User, 
            ingredient: Ingredient
            ) -> PantryItem:
        """
        Remove an ingredient from the user's pantry.

        Args:
            user(User): The ORM user object
            ingredient_name(str): The name of the ingredient
        
        Returns:
            Optional(PantryItem): The pantry item that was removed or None if it is not found.
        """
        item = user.remove_ingredient_from_pantry(ingredient)

        if item:
            self.db.commit_transaction()

        return item
    
    def update_pantry_item(
            self, 
            user: User, 
            ingredient: Ingredient, 
            quantity: Optional[int | None ]= None, 
            unit: str | None = None
            ) -> PantryItem | None:
        """
        Update the quantity or unit of items in the pantry.

        Args:
            user(User): The ORM User object.
            ingredient(Ingredient): The ORM Ingredient object.
            quantity(int): The amount of the ingredient.
            unit(str): The unit of the amount of the ingredient.

        Returns:
            Optional(PantryItem): The PantryItem or None
        """
        item = user.update_pantry_item(ingredient, quantity, unit)
        if item:
            self.db.commit_transaction()

        return item

class UserService:
    """
    
    """
    def __init__(self, db_query: DBQuery):
        self.db = db_query
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validates a password against rules:
        - A minimum of 8 characters
        - At least 3 out of 4 character types:
            - Uppercase
            - Lowercase
            - Digit
            - Special character
        """

        if len(password) < 8:
            print("Password is not long enough.")
            return False
        
        unique:int = 0

        if re.search(r"[A-Z]", password):
            unique += 1
        if re.search(r"[a-z]", password):
            unique += 1
        if re.search(r"\d", password):
            unique += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            unique += 1
        
        if unique >= 3:
            return True
        
        print("Password must include at least 3 of 4 types: uppercase, lowercase, digits, and special characters")
        return False

    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by emial

        Args:
            email(str): The user's email

        Returns:
            user(User): The User ORM object from the database.
        """
        user = (
            self.db.query(User)
            .filter_by(email = email)
            .first()
        )

        if user is None:
            return None
        
        return user
    
    def create_user(
            self, 
            email: str, 
            password: str
            ) -> User | None:
        if self.get_user_by_email(email) is not None:
            print("This user already exists.")
            return None
        
        user = User(email = email, password = password)
        
        if user is None:
            return None
        
        try:
            self.db.add(user)
            self.db.commit_transaction()
            return user
        except Exception as e:
            self.db.rollback_transaction()
            print(f"The transaction failed. User not created. Error: {e}")
            return None
        
    def delete_user(
            self, 
            user: User
            ) -> bool:
        if user is None:
            return False
        
        try:
            self.db.delete(user)
            self.db.commit_transaction()
            return True
        except Exception as e:
            print(f"Could not delete user. Error: {e}")
            self.db.rollback_transaction()
            return False

class IngredientService:
    """
    Ingredient services:
        find_ingredients: Locate ingredient
        add_ingredient: Add an ingredient to the database
        remove_ingredient: Remove an ingredient from the database
    """
    def __init__(self, db_query: DBQuery):
        self.db = db_query

    def find_ingredient(
            self, 
            name: str
            ) -> Ingredient | None:
        """
        Return the Ingredient object if it exists, else None.

        Args:
            name(str): The name of the ingredient

        Returns:
            Optional(Ingredient): The Ingredient or None is returned.
        """
        return (self.db.query(Ingredient)
                .filter_by(name = name)
                .first())
    
    def add_ingredient(
            self, 
            name: str
            ) -> Ingredient | None:
        """
        Add an ingredient to the database
        
        Args:
            name(str): The name of the ingredient
        """
        ingredient = self.find_ingredient(name)

        if ingredient is None:
            ingredient = Ingredient(name = name)
            self.db.add(ingredient)
            self.db.commit_transaction()

        return ingredient
    
    def remove_ingredient(
            self,
            name: str
            ) -> bool:
        """
        Remove an ingredient from the database.

        Args:
            name(str): The name of the ingredient.

        Returns:
            True if the Ingredient was deleted, False if it was not.
        """
        ingredient = self.find_ingredient(name)

        if ingredient is None:
            return False
        
        try:
            self.db.delete(ingredient)
            self.db.commit_transaction()
            return True
        except Exception as e:
            print("Error: Could not delete ingredient: {e}")
            self.db.rollback_transaction()
            return False
    
    def remove_ingredient_obj(
            self,
            ingredient: Ingredient
    ) -> bool:
        if ingredient is None:
            return False
        
        try:
            self.db.delete(ingredient)
            self.db.commit_transaction()
            return True
        except Exception as e:
            print("Error: No object to delete: {e}")
            self.db.rollback_transaction()
            return False

class RecipeService:
    """
    Recipe Services:
        - add_recipe
        - delete_recipe
        - add_ingredient_to_recipe
    """
    def __init__(self, db_query: DBQuery):
        self.db = db_query

    def find_recipe(
            self,
            name: str
            ) -> Recipe | None:
        return (self.db.
                query(Recipe).
                filter_by(name = name).
                first())
                

    def add_recipe(
            self,
            name:str,
            instructions: list[str],
            ingredients: Optional[list[Ingredient]] = None
            ) -> Recipe | None:
        """
        Add a recipe to the database.

        Args:
            name(str): Name of the recipe.
            instructions(str): Recipe instructions.
            ingredients(list(Ingredient)): List of ORM Ingredient objects.

        Returns:
            Recipe object if creation succeeded, else None
        """
        # Check if recipe already exists
        existing = self.find_recipe(name)

        if existing:
            print(f"A recipe with the name '{name}' already exists.")
            return None
        
        recipe = Recipe(name = name, 
                        instructions = instructions)

        if ingredients:
            recipe.ingredients.extend(ingredients)
        
        try:
            self.db.add(recipe)
            self.db.commit_transaction()
            return recipe
        except Exception as e:
            self.db.rollback_transaction()
            print(f"Failed to create recipe. Error: {e}")
            return None
        
    def delete_recipe(
            self,
            recipe: Recipe
            ) -> bool:
        """
        Delete a recipe from the database.

        Args:
            recipe(Recipe): The ORM object to delete from the database.

        Returns:
            True if deleted successfully, False otherwise.
        """
        try:
            self.db.delete(recipe)
            self.db.commit_transaction()
            return True
        except Exception as e:
            self.db.rollback_transaction()
            print(f"Failed to delete recipe. Error: {e}")
            return False
    
    def rate_recipe(self, user: User, recipe: Recipe, rating: int):
        """
        Add or update a rating for a recipe by a user.
        """

        try:
            rating_obj = user.rate_recipe(recipe, rating)
            self.db.commit_transaction()
            return rating_obj
        except Exception as e:
            self.db.rollback_transaction()
            print(f"Failed to rate recipe: {e}")
            return None
        
class ServiceContainer:
    def __init__(self):
        self.db_connect = DBConnect()
        self.db_query = DBQuery(self.db_connect)

        self.user_service = UserService(self.db_query)
        self.ingredient_service = IngredientService(self.db_query)
        self.pantry_service = PantryService(self.db_query)
        self.recipe_service = RecipeService(self.db_query)

    #User Service
    def create_user(
            self, 
            email: str, 
            password:str
        ) -> User | None:
        return self.user_service.create_user(email, password)
    
    def get_user_by_email(
            self, 
            email: str
        ) -> User | None:
        return self.user_service.get_user_by_email(email)
    
    def delete_user(
            self, 
            user: User
        ) -> bool:
        return self.user_service.delete_user(user)
    
    #Ingredient Service
    def add_ingredient(
            self, 
            name: str
        ) -> Ingredient | None:
        return self.ingredient_service.add_ingredient(name)
    
    def remove_ingredient(
            self, 
            name: str
        ) -> bool:
        return self.ingredient_service.remove_ingredient(name)
    
    def find_ingredient(
            self, 
            name: str
        ) -> Ingredient | None:
        return self.ingredient_service.find_ingredient(name)
    
    def remove_ingredient_obj(
            self, 
            ingredient: Ingredient
        ) -> bool:
        return self.ingredient_service.remove_ingredient_obj(ingredient)
    
    #Pantry Service
    def add_to_pantry(
            self,
            user: User,
            ingredients: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.add_ingredient_to_pantry(
            user, ingredients, quantity, unit
        )
    
    def remove_from_pantry(
            self,
            user: User,
            ingredient: Ingredient
    ) -> PantryItem | None:
        return self.pantry_service.remove_ingredient_from_pantry(
            user, ingredient
        )
    
    def update_pantry(
            self,
            user: User,
            ingredient: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.update_pantry_item(
            user, ingredient, quantity, unit
        )
    
    #Recipe Service
    def add_recipe(
            self,
            name: str,
            instructions: list[str],
            ingredients: Optional[list[Ingredient]] = None
    ) -> Recipe | None:
        return self.recipe_service.add_recipe(
            name, instructions, ingredients
        )
    
    def delete_recipe(self, recipe: Recipe) -> bool:
        return self.recipe_service.delete_recipe(recipe)

    def find_recipe(self, name: str) -> Recipe | None:
        return self.recipe_service.find_recipe(name)

    def rate_recipe(
        self,
        user: User,
        recipe: Recipe,
        rating: int
    ):
        return self.recipe_service.rate_recipe(user, recipe, rating)

    # ==================== DB CONTROL ==================== #

    def reset_database(self):
        self.db_connect.drop_tables()
        self.db_connect.create_tables()

    def close(self):
        """
        Use this to close the database connection at application
        close.
        """
        from sqlalchemy.orm import Session
        self.db_query.close()
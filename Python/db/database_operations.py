"""
    Author: Jon Bailey
"""

from db.db_connect import DBConnect
from db.unit_of_work import UnitOfWork
from model import Ingredient, User, PantryItem, Recipe, recipe_ingredients, user_favorites
import re
from typing import Optional
from sqlalchemy.orm import Session

class PantryService:
    """
    A service layer for database operations using the pantry.
    """
    def __init__(self):
        pass
    
    def add_ingredient_to_pantry(
            self, 
            user_id: int, 
            ingredient_name: str, 
            quantity: Optional[int] = None, 
            unit: Optional[str] = None
            ) -> PantryItem:
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
        with UnitOfWork() as uow:
            user: User = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            ingredient: Ingredient = uow.ingredients.get_by_name(ingredient_name)
            if not ingredient:
                ingredient = Ingredient(name = ingredient_name)
                uow.ingredients.add(ingredient)
            
            pantry_item = user.add_ingredient_to_pantry(
                ingredient,
                quantity,
                unit
            )
            uow.commit()
            return pantry_item
    
    def remove_ingredient_from_pantry(
            self, 
            user_id: int, 
            ingredient_name: str
            ) -> Optional[PantryItem]:
        """
        Remove an ingredient from the user's pantry.

        Args:
            user(User): The ORM user object
            ingredient_name(str): The name of the ingredient
        
        Returns:
            Optional(PantryItem): The pantry item that was removed or None if it is not found.
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            ingredient = uow.ingredients.get_by_name(ingredient_name)
            if not ingredient:
                return None
            
            item = user.remove_ingredient_from_pantry(ingredient)

            if item:
                uow.commit()

            return item
    
    def update_pantry_item(
            self, 
            user_id: int, 
            ingredient_name: str, 
            quantity: Optional[int]= None, 
            unit: Optional[str] = None
            ) -> Optional[PantryItem]:
        """
        Update the quantity or unit of items in the pantry.

        Args:
            user(User): The user id from a user account.
            ingredient_name(str): The ingredient item's name
            quantity(int): The amount of the ingredient.
            unit(str): The unit of the amount of the ingredient.

        Returns:
            Optional(PantryItem): The PantryItem or None
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            ingredient = uow.ingredients.get_by_name(ingredient_name)
            if not ingredient:
                return None
            
            item = user.update_pantry_item(ingredient, quantity, unit)

            if item:
                uow.commit()

            return item

class UserService:
    """
    A service layer for database operations using the user.
    """
    def __init__(self):
        pass
    
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
        Retrieve a user by email

        Args:
            email(str): The user's email

        Returns:
            user(User): The User ORM object from the database.
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_email(email)
        
            return user
        
    def get_user_by_id(
            self,
            user_id: int
    ) -> Optional[User]:
        """
        If you need it, you can find Users by ID as well.
        """
        with UnitOfWork() as uow:
            return uow.users.get_by_id(user_id)
    
    def create_user(
            self, 
            email: str, 
            password: str
            ) -> Optional[User]:
        with UnitOfWork() as uow:
            if uow.users.get_by_email(email):
                raise ValueError("User already exists.")
            
            if not self.validate_password(password):
                raise ValueError("User password is not strong enough")

            user = User(email = email, password = password)

            uow.users.add(user)
            uow.commit()
            
            return user
        
    def delete_user(
            self, 
            user_id: int
            ) -> bool:
        """
        
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)

            if not user:
                return False
            
            uow.users.delete(user)
            uow.commit()
            return True
        
    def authenticate_user(
            self,
            email: str,
            password: str
    ) -> Optional[User]:
        with UnitOfWork() as uow:
            user = uow.users.get_by_email(email)

            if not user:
                return None
            
            if not user.check_password(password):
                return None
            
            return user

class IngredientService:
    """
    Ingredient services:
        find_ingredients: Locate ingredient
        add_ingredient: Add an ingredient to the database
        remove_ingredient: Remove an ingredient from the database
    """
    def __init__(self):
        pass

    def find_ingredient(
            self, 
            name: str
            ) -> Optional[Ingredient]:
        """
        Return the Ingredient object if it exists, else None.

        Args:
            name(str): The name of the ingredient

        Returns:
            Optional(Ingredient): The Ingredient or None is returned.
        """
        with UnitOfWork() as uow:
            return uow.ingredients.get_by_name(name)
    
    def add_ingredient(
            self, 
            name: str
            ) -> Optional[Ingredient]:
        """
        Add an ingredient to the database
        
        Args:
            name(str): The name of the ingredient
        """
        with UnitOfWork() as uow:
            ingredient = uow.ingredients.get_by_name(name)

            if ingredient is None:
                ingredient = Ingredient(name = name)
                uow.ingredients.add(ingredient)

            uow.commit()
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
        with UnitOfWork() as uow:
            ingredient = uow.ingredients.get_by_name(name)
            if not ingredient:
                return False
            
            uow.ingredients.delete(ingredient)
            uow.commit()
            return True
    
    def remove_ingredient_obj(
            self,
            ingredient: Ingredient
        ) -> bool:
        if ingredient is None:
            return False
        
        assert type(ingredient) is Ingredient
        
        with UnitOfWork() as uow:
            assert type(uow.session) is Session
            ingredient = uow.session.merge(ingredient)
            uow.ingredients.delete(ingredient)
            uow.commit()
            return True
    
    def get_ingredient_by_id(
            self,
            ing_id: int
    ) -> Ingredient:
        with UnitOfWork() as uow:
            return uow.ingredients.get_by_id(ing_id)


class RecipeService:
    """
    Recipe Services:
        - add_recipe
        - delete_recipe
        - add_ingredient_to_recipe
    """
    def __init__(self):
        pass

    def find_recipe(
            self,
            name: str
            ) -> Recipe | None:
        with UnitOfWork() as uow:
            return uow.recipes.get_by_name(name)
                

    def add_recipe(
            self,
            name:str,
            instructions: list[str],
            ingredients: list[str]
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
        with UnitOfWork() as uow:
            recipe = uow.recipes.get_by_name(name)
            if recipe:
                return recipe
            
            recipe = Recipe(name = name, instructions = instructions or [])
            uow.recipes.add(recipe)

            for ingredient in ingredients or []:
                ing = uow.ingredients.get_by_name(ingredient)
                if not ing:
                    ing = Ingredient(name = ingredient)
                    uow.ingredients.add(ing)
                if ing not in recipe.ingredients:
                    recipe.ingredients.append(ing)

            uow.commit()
            return recipe
        
    def delete_recipe(
            self,
            recipe_id: int
            ) -> bool:
        """
        Delete a recipe from the database.

        Args:
            recipe(Recipe): The ORM object to delete from the database.

        Returns:
            True if deleted successfully, False otherwise.
        """
        with UnitOfWork() as uow:
            recipe = uow.recipes.get_by_id(recipe_id)
            if not recipe:
                return False
            
            uow.recipes.delete(recipe)
            uow.commit()
            return True
    
    def add_ingredient_to_recipe(
            self,
            recipe_id: int,
            ingredient_name: str
    ) -> Recipe:
        """
        Add an ingredient to the recipe.
        """
        with UnitOfWork() as uow:
            recipe = uow.recipes.get_by_id(recipe_id)
            if not recipe:
                raise ValueError("Recipe not found")
            
            ingredient = uow.ingredients.get_by_name(ingredient_name)
            if not ingredient:
                ingredient = Ingredient(name = ingredient_name)
                uow.ingredients.add(ingredient)
            
            if ingredient not in recipe.ingredients:
                recipe.ingredients.append(ingredient)

            uow.commit()
            return recipe

    
    def rate_recipe(
            self, 
            user_id: int, 
            recipe_id: int, 
            rating: int
        ) -> None:
        """
        Add or update a rating for a recipe by a user.
        """
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        
        with UnitOfWork() as uow:
            recipe = uow.recipes.get_by_id(recipe_id)
            if not recipe:
                raise ValueError("Recipe not found")
            
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            recipe.add_rating(user, rating)
            uow.commit()
    
    def get_all_recipes(self) -> list[Recipe]:
        """
        Retrieve all recipes from the database. Implementation of 
        the Retrieve Recipes use case.
        """
        with UnitOfWork() as uow:
            recipes = uow.recipes.get_all()
            return recipes
        
class ServiceContainer:
    def __init__(self):
        self.db_connect = DBConnect()

        self.user_service = UserService()
        self.ingredient_service = IngredientService()
        self.pantry_service = PantryService()
        self.recipe_service = RecipeService()

    #User Service
    def create_user(
            self, 
            email: str, 
            password:str
        ) -> Optional[User]:
        return self.user_service.create_user(email, password)
    
    def get_user_by_email(
            self, 
            email: str
        ) -> User | None:
        """
        Return a User via email. Do not use this method to log people in. Use the
        authenticate_user method in the same class.
        """
        return self.user_service.get_user_by_email(email)
    
    def delete_user(
            self, 
            user: User
        ) -> bool:
        """
        Delete the user from the database.
        """
        return self.user_service.delete_user(user.get_id())
    
    def authenticate_user(
            self, 
            email: str,
            password: str
    ) -> Optional[User]:
        """
        Authenticate the user's password to log them in.
        """
        return self.user_service.authenticate_user(email, password)
    
    def get_user_by_id(
            self,
            user_id: int
    ) -> Optional[User]:
        """
        Find a user from their user id.
        """
        return self.user_service.get_user_by_id(user_id)
    
    #Ingredient Service
    def add_ingredient(
            self, 
            name: str
        ) -> Optional[Ingredient]:
        return self.ingredient_service.add_ingredient(name)
    
    def remove_ingredient(
            self, 
            name: str
        ) -> bool:
        return self.ingredient_service.remove_ingredient(name)
    
    def find_ingredient(
            self, 
            name: str
        ) -> Optional[Ingredient]:
        return self.ingredient_service.find_ingredient(name)
    
    def remove_ingredient_obj(
            self, 
            ingredient: Ingredient
        ) -> bool:
        return self.ingredient_service.remove_ingredient_obj(ingredient)
    
    def get_ingredient_by_id(
            self,
            ing_id: int
    ) -> Ingredient:
        return self.ingredient_service.get_ingredient_by_id(ing_id)
    
    #Pantry Service
    def add_to_pantry(
            self,
            user: User,
            ingredients: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.add_ingredient_to_pantry(
            user.get_id(), 
            ingredients.get_name(), 
            quantity, 
            unit
        )
    
    def remove_from_pantry(
            self,
            user: User,
            ingredient: Ingredient
    ) -> Optional[PantryItem]:
        return self.pantry_service.remove_ingredient_from_pantry(
            user.get_id(), 
            ingredient.get_name()
        )
    
    def update_pantry(
            self,
            user: User,
            ingredient: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.update_pantry_item(
            user.get_id(), 
            ingredient.get_name(), 
            quantity, 
            unit
        )
    
    #Recipe Service
    def add_recipe(
            self,
            name: str,
            instructions: list[str],
            ingredients: Optional[list[Ingredient]] = None
    ) -> Recipe | None:
        ingredient_list = []
        if ingredients:
            for ingredient in ingredients:
                ingredient_list.append(ingredient.get_name())

        recipe = self.recipe_service.add_recipe(
            name, 
            instructions,
            ingredient_list
        )
        if recipe is None:
            raise RuntimeError("Failed to create Recipe")
        return recipe
    
    def delete_recipe(self, recipe_id: int) -> bool:
        return self.recipe_service.delete_recipe(recipe_id)

    def find_recipe(self, name: str) -> Recipe | None:
        return self.recipe_service.find_recipe(name)
    
    def add_ingredient_to_recipe(
            self,
            recipe_id: int,
            ingredient_name: str
    ) -> Recipe:
        """
        Add an ingredient to the recipe.
        """
        return self.recipe_service.add_ingredient_to_recipe(recipe_id, ingredient_name)

    def rate_recipe(
        self,
        user_id: int,
        recipe_id: int,
        rating: int
    ):
        """
        Add or update a rating for a recipe by a user.
        """
        return self.recipe_service.rate_recipe(user_id, recipe_id, rating)
    
    def get_all_recipes(self) -> list[Recipe]:
        """
        Retrieve all recipes from the database.
        """
        return self.recipe_service.get_all_recipes()

    # ==================== DB CONTROL ==================== #

    def reset_database(self):
        """
        This option will drop the entire database and rebuild columns ONLY.

        Only run this if you want to delete everything.
        """
        self.db_connect.drop_tables()
        self.db_connect.create_tables()

    def close(self):
        """
        Use this to close the database connection at application
        close.
        """
        from sqlalchemy.orm import Session
        self.db_connect.shutdown()
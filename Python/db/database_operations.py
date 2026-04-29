"""
    Author: Jon Bailey
"""

from db.db_connect import DBConnect
from db.unit_of_work import UnitOfWork
from model import Ingredient, User, PantryItem, Recipe, user_favorites, RecipeIngredient, UserRecipeNote, Rating, UserSearch
import re
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import Row
from datetime import datetime

class PantryService:
    """
    A service layer for database operations using the pantry.
    """
    def __init__(self):
        pass
    
    def add_ingredient_to_pantry(
            self, 
            user: "User", 
            ingredient: "Ingredient", 
            quantity: Optional[float] = None, 
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
            item = user.add_ingredient_to_pantry(
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
            uow.commit()
        return item
            
    
    def remove_ingredient_from_pantry(
            self, 
            user: User, 
            ingredient: Ingredient
            ) -> Optional[PantryItem]:
        """
        Remove an ingredient from the user's pantry.

        Args:
            user(User): The ORM user object
            ingredient: The ORM ingredient object
        
        Returns:
            Optional(PantryItem): The pantry item that was removed or None if it is not found.
        """
        with UnitOfWork() as uow:
            item = user.remove_ingredient_from_pantry(ingredient=ingredient)
            if item:
                uow.commit()
        return item
            
    
    def update_pantry_item(
            self, 
            user: User, 
            ingredient: Ingredient, 
            quantity: Optional[int] = None, 
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
            item = user.update_pantry_item(
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
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
            if not self.validate_password(password):
                raise ValueError("User password is not strong enough")
            
            if uow.users.get_by_email(email):
                raise ValueError("User already exists.")
            
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

    def add_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
    ) -> list[str]:
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)
            db_recipe = uow.recipes.get_by_id(recipe.id)

            if db_user is None:
                raise ValueError("Could not find User")
            
            if db_recipe is None:
                raise ValueError("Could not find Recipe")

            item = db_user.add_note(db_recipe, note)
            
            uow.commit()

            return item
        
    def delete_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
        ) -> list[str]:
        """
        Remove a specific note for a given recipe.

        Returns:
            Updated list of notes.
        """
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)
            db_recipe = uow.recipes.get_by_id(recipe.id)

            if db_user is None:
                raise ValueError("User not found")
            if db_recipe is None:
                raise ValueError("Recipe not found")
            
            updated_notes = db_user.remove_note(db_recipe, note)

            uow.commit()

            return updated_notes


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
        name: str,
        instructions: Optional[List[str]] = None,
        ingredients: Optional[list[str]] = None,
        pub_time: Optional[datetime] = None
        ) -> Recipe | None:
        pass
        
    def add_recipe(
        self,
        name: str,
        instructions: Optional[List[str]] = None,
        ingredients: Optional[list[str]] = None,
        pub_time: Optional[datetime] = None
        ) -> Recipe | None:

        """
        ingredients format:
        [
            {"name": "Flour", "quantity": 2, "unit": "cups"},
            {"name": "Milk", "quantity": 1, "unit": "cup"}
        ]
        """

        with UnitOfWork() as uow:
            recipe = uow.recipes.get_by_name(name)
            if recipe:
                return recipe
                
            recipe = Recipe(
                name=name,
                instructions=instructions or [],
                ingredients=[],
                pub_time=pub_time
            )
            uow.recipes.add(recipe)

            if ingredients is None:
                uow.commit()
                return recipe
            
            recipe = Recipe(name=name, ingredients=items, instructions=instructions or [], pub_time=pub_time)

            for ing_name in ingredients:
                ingredient = uow.ingredients.get_by_name(ing_name)

                if not ingredient:
                    ingredient = Ingredient(name=ing_name)
                    uow.ingredients.add(ingredient)
                    if uow.session is not None:
                        uow.session.flush()

                recipe.add_ingredient(ingredient)

            uow.recipes.add(recipe)
            uow.commit()
            return recipe
        
    def delete_recipe(
            self,
            recipe_id: int
            ) -> bool:
        """
        Delete a recipe from the database.

        Args:
            recipe_id(int): The recipe id to delete.

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

    #-save to favorites/favorites methods

    def add_recipe_to_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        """
        Add a recipe to a user's favorites.
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            recipe = uow.recipes.get_by_id(recipe_id)
            if not recipe:
                raise ValueError("Recipe not found")
            
            added = user.add_favorite_recipe(recipe)

            if added:
                uow.commit()

            return added
    
    def remove_recipe_from_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        """
        Remove a recipe from a user's favorites.
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            recipe = uow.recipes.get_by_id(recipe_id)
            if not recipe:
                raise ValueError("Recipe not found")
            
            removed = user.remove_favorite_recipe(recipe)

            if removed:
                uow.commit()

            return removed
    
    def get_user_favorites(
            self,
            user_id: int
            ) -> list[Recipe]:
        """
        Get all favorite recipes for a user.
        """
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            return user.get_favorite_recipes()
    #-------------------
        
    
class SearchService:
    """
    A class to contain services related to searches.
    """

    def record_search(
            self, 
            user: User, 
            query: str):
        query = query.strip().lower()
        with UnitOfWork() as uow:

            search = UserSearch(
                user_id = user.id if user else None,
                query = query
            )
            
            uow.searches.add(search)
            uow.commit()
    
    def get_popular_searches(
            self, 
            limit: int = 10
            ) -> list[Row[tuple[str, int]]]:
        with UnitOfWork() as uow:
            result = uow.searches.get_popular(limit = limit)
            return result
    
    def get_recent_searches(
            self,
            limit: int = 50
    ) -> list[UserSearch]:
        with UnitOfWork() as uow:
            result = uow.searches.get_recent(limit = limit)
            return result

class ServiceContainer:
    def __init__(self):
        self.db_connect = DBConnect()

        self._user_service = UserService()
        self._ingredient_service = IngredientService()
        self._pantry_service = PantryService()
        self._recipe_service = RecipeService()
        self._search_service = SearchService()

    @property
    def user_service(self):
        return self._user_service
    
    @property
    def ingredient_service(self):
        return self._ingredient_service
    
    @property
    def pantry_service(self):
        return self._pantry_service
    
    @property
    def recipe_service(self):
        return self._recipe_service
    
    @property
    def search_service(self):
        return self._search_service

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
    
    def add_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
    ) -> list[str]:
        return self.user_service.add_personal_note(user = user, recipe = recipe, note = note)
    
    def delete_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
    ) -> list[str]:
        return self.user_service.delete_personal_note(user = user, recipe = recipe, note = note)
    
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
            ingredient: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> Optional[PantryItem]:
        return self.pantry_service.add_ingredient_to_pantry(
            user, 
            ingredient, 
            quantity, 
            unit
        )
    
    def remove_from_pantry(
            self,
            user: User,
            ingredient: Ingredient
    ) -> Optional[PantryItem]:
        return self.pantry_service.remove_ingredient_from_pantry(
            user, 
            ingredient
        )
    
    def update_pantry(
            self,
            user: User,
            ingredient: Ingredient,
            quantity: Optional[int] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.update_pantry_item(
            user, 
            ingredient, 
            quantity, 
            unit
        )
    
    #Recipe Service
    def add_recipe(
            self,
            name: str,
            instructions: list[str],
            ingredients: Optional[list[str]] = None,
            pub_time: Optional[datetime] = None
    ) -> Recipe | None:

        recipe = self.recipe_service.add_recipe(
            name, 
            instructions,
            ingredients = ingredients,
            pub_time = pub_time
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
    
    # ==================== Searches ====================== #

    def record_search(
            self,
            user: User, 
            query: str
    ):
        self.search_service.record_search(user, query)

    def get_popular_searches(
            self,
            limit: int
    ) -> list[Row[tuple[str, int]]]:
        """
        Get the most popular searches.

        Parameters:
            limit(int): The number of items you want to return.
        
        Returns:
            list(Row(tuple(str, int))): A list of rows that contain a tuple with the name and the count of the search terms.
        """
        return self.search_service.get_popular_searches(limit = limit)
        

    #---------------- lu: STF Block | favorites container methods
    def add_recipe_to_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        return self.recipe_service.add_recipe_to_favorites(user_id, recipe_id)
    
    def remove_recipe_from_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        return self.recipe_service.remove_recipe_from_favorites(user_id, recipe_id)
    
    def get_user_favorites(
            self,
            user_id: int
            ) -> list[Recipe]:
        return self.recipe_service.get_user_favorites(user_id)
    #----------


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

    
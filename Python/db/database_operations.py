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
from typing import TypedDict

class PopularSearch(TypedDict):
    query: str
    count: int

class Pantry(TypedDict):
    index: int
    ingredient_id: int
    ingredient_name: str
    quantity: float | None
    unit: str | None

# By Jon Bailey
class PantryService:
    """
    A service layer for database operations using the pantry.
    """
    def __init__(self):
        pass
    
    #By Jon Bailey
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
            db_user = uow.users.get_by_id(user.id)

            if db_user is None:
                raise ValueError("User does not exist")

            item = db_user.add_ingredient_to_pantry(
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
            uow.commit()
        return item
            
    #By Jon Bailey
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
            db_user = uow.users.get_by_id(user.id)

            if db_user is None:
                raise ValueError("User not found")

            item = db_user.remove_ingredient_from_pantry(ingredient)

            if item:
                uow.commit()

            return item
            
    #By Jon Bailey
    def update_pantry_item(
            self, 
            user: User, 
            ingredient: Ingredient, 
            quantity: Optional[float] = None, 
            unit: Optional[str] = None
        ) -> Optional[PantryItem]:

        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)
            db_ingredient = uow.ingredients.get_by_id(ingredient.id)

            if db_user is None:
                raise ValueError("User not found")
            
            if db_ingredient is None:
                raise ValueError("Ingtredient not found")

            item = db_user.update_pantry_item(
                ingredient=db_ingredient,
                quantity=quantity,
                unit=unit
            )

            if item:
                uow.commit()

            return item
    
    #By Jon Bailey
    def get_all_pantry_items(
            self,
            user: User
    ) -> list[Pantry]:
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)

            if db_user is None:
                raise ValueError("User does not exist")

            pantry_items = list(db_user._pantry.values())

            return [
                {
                    "index": i,
                    "ingredient_id": item.ingredient.id,
                    "ingredient_name": item.ingredient.name,
                    "quantity": item.quantity,
                    "unit": item.unit
                }
                for i, item in enumerate(pantry_items)
            ]
    
    def get_pantry_item_by_index(self, user: User, index: int) -> PantryItem:
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)

            if db_user is None:
                raise ValueError("User does not exist")

            pantry_items = list(db_user._pantry.values())

            if index < 0 or index >= len(pantry_items):
                raise ValueError("Invalid pantry index")

            return pantry_items[index]

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

    #By Thanvii Ambala
    def change_password(self, user: User, new_password: str) -> bool:
        """
        Change the user's password.

        Args:
            user(User): The ORM user object.
            new_password(str): The new password to set.

        Returns:
            True if the password was changed successfully, False otherwise.
        """
        if not self.validate_password(new_password):
            return False
        
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)

            if db_user is None:
                raise ValueError("User not found")
            
            db_user.reset_password(new_password)
            uow.commit()
            return True
        
    #By Thanvii Ambala
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
    
    #By Jon Bailey
    def get_user_by_id(
            self,
            user_id: int
    ) -> Optional[User]:
        """
        If you need it, you can find Users by ID as well.
        """
        with UnitOfWork() as uow:
            return uow.users.get_by_id(user_id)
    
    #By Jon Bailey
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
    
    #By Jon Bailey
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
    
    #By Jon Bailey
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

    #By Jon Bailey
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
    
    #By Jon Bailey
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

    #By Jon Bailey
    def get_all_user_notes(self, user_id: int) -> list[tuple[Recipe, str]]:
        with UnitOfWork() as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
    
            result = []
            for recipe, notes in user.notes.items():
                for note in notes:
                    result.append((recipe, note))

            return result

class IngredientService:
    """
    Ingredient services:
        find_ingredients: Locate ingredient
        add_ingredient: Add an ingredient to the database
        remove_ingredient: Remove an ingredient from the database
    """
    def __init__(self):
        pass

    #By Jon Bailey
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
    
    #By Jon Bailey
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
    
    #By Jon Bailey
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
    
    #By Jon Bailey
    def remove_ingredient_obj(
            self,
            ingredient: Ingredient
        ) -> bool:
        if ingredient is None:
            return False
        
        with UnitOfWork() as uow:
            db_ingredient = uow.ingredients.get_by_id(ingredient.id)

            if not db_ingredient:
                return False
            
            uow.ingredients.delete(db_ingredient)
            uow.commit()
            return True
    
    #By Jon Bailey
    def get_ingredient_by_id(
            self,
            ing_id: int
    ) -> Optional[Ingredient]:
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

    #By Jon Bailey
    def find_recipe(
            self,
            name: str
            ) -> list[Recipe]:
        with UnitOfWork() as uow:
            return uow.recipes.search_by_name(name)
    
    #By Jon Bailey
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
            existing = uow.recipes.get_by_name(name)
            
            if existing:
                return existing
                
            recipe = Recipe(
                name=name,
                instructions=instructions or [],
                ingredients=[],
                pub_time=pub_time
            )
            uow.recipes.add(recipe)

            if ingredients:
                for ing_name in ingredients:
                    ingredient = uow.ingredients.get_by_name(ing_name)

                    if not ingredient:
                        ingredient = Ingredient(name=ing_name)
                        uow.ingredients.add(ingredient)
                        if uow.session is not None:
                            uow.session.flush()

                    recipe.add_ingredient(ingredient)

            uow.commit()
            return recipe
    
    #By Jon Bailey
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
    
    #By Thanvii Ambala
    def find_recipes_by_pantry(
            self,
            user: User
    ) -> list[Recipe]:
        """
        Return recipes that can be made using ONLY the ingredients
        available in the user's pantry.

        Args:
          pantry: list of ingredient names the user currently has at home
        """
        with UnitOfWork() as uow:
            db_user = uow.users.get_by_id(user.id)
            if db_user is None:
                raise ValueError("User not found")
            pantry_ingredients_ids = [item.ingredient.id for item in db_user._pantry.values()]
            all_recipes = uow.recipes.get_all()
            matching_recipes = []
            for recipe in all_recipes:
                recipe_ingredient_ids = set(recipe._ingredients.keys())
                if recipe_ingredient_ids.issubset(pantry_ingredients_ids):
                    matching_recipes.append(recipe)
            return matching_recipes
        
    #By Thanvii Ambala
    def search_recipe_by_criteria(
        self,
        include_ingredients: list[str],
        exclude_ingredients: list[str],
        category: str | None,
        dietary_requirements: list[str]
    ) -> list[Recipe]:
        with UnitOfWork() as uow:
            all_recipes = uow.recipes.get_all()
            include_set = {name.strip().lower() for name in include_ingredients}
            exclude_set = {name.strip().lower() for name in exclude_ingredients}
            diet_set = {tag.strip().lower() for tag in dietary_requirements}
            results = []
            for recipe in all_recipes:
                # -------------------------
                # INGREDIENT SET
                # -------------------------
                recipe_ing_names = {
                    ri.ingredient.name.strip().lower()
                    for ri in recipe._ingredients.values()
                }
                # include check (must contain ALL)
                if include_set and not include_set.issubset(recipe_ing_names):
                    continue
                # exclude check (must contain NONE)
                if exclude_set.intersection(recipe_ing_names):
                    continue
                # -------------------------
                # CATEGORY CHECK
                # -------------------------
                if category:
                    if not recipe.category or recipe.category.strip().lower() != category.strip().lower():
                        continue
                # -------------------------
                # DIETARY TAGS CHECK
                # -------------------------
                recipe_tags = set(recipe.tags or [])
                recipe_tags = {t.strip().lower() for t in recipe_tags}
                if diet_set and not diet_set.issubset(recipe_tags):
                    continue
                results.append(recipe)
            return results
    
    #By Thanvii Ambala
    def find_recipes_by_ingredients(
            self,
            ingredients: list[str]
    ) -> list[Recipe]:
        with UnitOfWork() as uow:
            all_recipes = uow.recipes.get_all()
            if not ingredients:
                return all_recipes
            names = [ing.strip().lower() for ing in ingredients]
            search_ingredients = [uow.ingredients.get_by_name(name) for name in names]
            matching_recipes = []
            search_ingredients = [ing for ing in search_ingredients if ing is not None]
            if len(search_ingredients) != len(ingredients):
                return []  # If any ingredient is not found, return empty list
            ingredient_ids = {ing.id for ing in search_ingredients}
            for recipe in all_recipes:
                recipe_ingredient_ids = set(recipe._ingredients.keys())
                if ingredient_ids.issubset(recipe_ingredient_ids):
                    matching_recipes.append(recipe)
            return matching_recipes 

    def get_recipe_by_id(
            self,       
            recipe_id: int
    ) -> Optional[Recipe]:
        """
        Retrieve a recipe by its ID.

         Args:
            recipe_id: The unique number that identifies the recipe.

        Returns:
            A Recipe object, or None if not found.
        """
        with UnitOfWork() as uow:
            return uow.recipes.get_by_id(recipe_id)
    
    #By Thanvii Ambala
    def find_recipes_by_category(
            self,
            category: str
    ) -> list[Recipe]:
        with UnitOfWork() as uow:
            all_recipes = uow.recipes.get_all()
            category_lower = category.strip().lower()
            matching_recipes = []
            for recipe in all_recipes:
                if recipe.category and recipe.category.strip().lower() == category_lower:
                    matching_recipes.append(recipe) 
            return matching_recipes 

    #By Thanvii Ambala        
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

    #By Jon Bailey
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
    
    #By Jon Bailey
    def get_all_recipes(self) -> list[Recipe]:
        """
        Retrieve all recipes from the database. Implementation of 
        the Retrieve Recipes use case.
        """
        with UnitOfWork() as uow:
            recipes = list(uow.recipes.get_all())
            return recipes

    #-save to favorites/favorites methods
    #By Lu
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
        
    #By Lu
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
    #By Lu
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
            
            favorites = list(user.favorites)
            
            return favorites
    #-------------------
        
    
class SearchService:
    """
    A class to contain services related to searches.
    """
    #By Jon Bailey
    def record_search(
            self, 
            query: str):
        query = query.strip().lower()
        with UnitOfWork() as uow:

            search = UserSearch(
                query = query
            )
            
            uow.searches.add(search)
            uow.commit()

    #By Jon Bailey
    def get_popular_searches(
            self, 
            limit: int = 10
            ) -> list[PopularSearch]:
        with UnitOfWork() as uow:
            return [
                {
                    "query": row [0],
                    "count": row[1]
                }
                for row in uow.searches.get_popular(limit = limit)
            ]
        
    #By Jon Bailey
    def get_recent_searches(
            self,
            limit: int = 50
    ) -> list[UserSearch]:
        with UnitOfWork() as uow:
            result = uow.searches.get_recent(limit = limit)
            return result

class ServiceContainer:
    #By Jon Bailey
    def __init__(self):
        self.db_connect = DBConnect()

        self._user_service = UserService()
        self._ingredient_service = IngredientService()
        self._pantry_service = PantryService()
        self._recipe_service = RecipeService()
        self._search_service = SearchService()

    #By Jon Bailey
    @property
    def user_service(self):
        return self._user_service
    
    #By Jon Bailey
    @property
    def ingredient_service(self):
        return self._ingredient_service
    
    #By Jon Bailey
    @property
    def pantry_service(self):
        return self._pantry_service
    
    #By Jon Bailey
    @property
    def recipe_service(self):
        return self._recipe_service
    
    #By Jon Bailey
    @property
    def search_service(self):
        return self._search_service

    #User Service
    #By Jon Bailey
    def create_user(
            self, 
            email: str, 
            password:str
        ) -> Optional[User]:
        return self.user_service.create_user(email, password)
    
    #By Thanvii Ambala
    def change_password(
            self,
            user: User,
            new_password: str
    ) -> bool:
        return self.user_service.change_password(user, new_password)
    
    #By Thanvii Ambala
    def get_user_by_email(
            self, 
            email: str
        ) -> User | None:
        """
        Return a User via email. Do not use this method to log people in. Use the
        authenticate_user method in the same class.
        """
        return self.user_service.get_user_by_email(email)
    
    #By Jon Bailey
    def delete_user(
            self, 
            user: User
        ) -> bool:
        """
        Delete the user from the database.
        """
        return self.user_service.delete_user(user.get_id())
    
    #By Jon Bailey
    def authenticate_user(
            self, 
            email: str,
            password: str
    ) -> Optional[User]:
        """
        Authenticate the user's password to log them in.
        """
        return self.user_service.authenticate_user(email, password)
    
    #By Jon Bailey
    def get_user_by_id(
            self,
            user_id: int
    ) -> Optional[User]:
        """
        Find a user from their user id.
        """
        return self.user_service.get_user_by_id(user_id)
    
    #By Jon Bailey
    def add_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
    ) -> list[str]:
        return self.user_service.add_personal_note(user = user, recipe = recipe, note = note)
    
    #By Jon Bailey
    def delete_personal_note(
            self,
            user: User,
            recipe: Recipe,
            note: str
    ) -> list[str]:
        return self.user_service.delete_personal_note(user = user, recipe = recipe, note = note)
    
    #By Jon Bailey
    def update_note(
            self,
            user: User,
            recipe: Recipe,
            old_note: str,
            new_note: str
    ) -> list[str]:
        self.user_service.delete_personal_note(user, recipe, old_note)
        return self.user_service.add_personal_note(user, recipe, new_note)
    
    #By Jon Bailey
    def get_all_user_notes(
            self, 
            user: User
        ) -> list[tuple[Recipe, str]]:
            return self.user_service.get_all_user_notes(user.id)
    
    #Ingredient Service
    def add_ingredient(
            self, 
            name: str
        ) -> Optional[Ingredient]:
        return self.ingredient_service.add_ingredient(name)
    
    #By Jon Bailey
    def remove_ingredient(
            self, 
            name: str
        ) -> bool:
        return self.ingredient_service.remove_ingredient(name)
    
    #By Jon Bailey
    def find_ingredient(
            self, 
            name: str
        ) -> Optional[Ingredient]:
        return self.ingredient_service.find_ingredient(name)
    
    #By Jon Bailey
    def remove_ingredient_obj(
            self, 
            ingredient: Ingredient
        ) -> bool:
        return self.ingredient_service.remove_ingredient_obj(ingredient)
    
    #By Jon Bailey
    def get_ingredient_by_id(
            self,
            ing_id: int
    ) -> Ingredient:
        return self.ingredient_service.get_ingredient_by_id(ing_id)
    
    #Pantry Service
    #By Jon Bailey
    def add_to_pantry(
            self,
            user: User,
            ingredient: Ingredient,
            quantity: Optional[float] = None,
            unit: Optional[str] = None
    ) -> Optional[PantryItem]:
        return self.pantry_service.add_ingredient_to_pantry(
            user, 
            ingredient, 
            quantity, 
            unit
        )
    
    #By Jon Bailey
    def remove_from_pantry(
            self,
            user: User,
            ingredient: Ingredient
    ) -> Optional[PantryItem]:
        return self.pantry_service.remove_ingredient_from_pantry(
            user, 
            ingredient
        )
    
    #By Jon Bailey
    def update_pantry(
            self,
            user: User,
            ingredient: Ingredient,
            quantity: Optional[float] = None,
            unit: Optional[str] = None
    ) -> PantryItem | None:
        return self.pantry_service.update_pantry_item(
            user, 
            ingredient, 
            quantity, 
            unit
        )
    
    #By Jon Bailey
    def get_all_pantry_items(
            self,
            user: User
    ) -> list[Pantry]:
        return self.pantry_service.get_all_pantry_items(user)
    
    #Recipe Service
    #By Jon Bailey
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
    
    #By Thanvii Ambala
    def find_recipes_by_ingredients(
            self, 
            ingredients: list[str]
        ) -> list[Recipe]:
        return self.recipe_service.find_recipes_by_ingredients(ingredients)
    
    #By Thanvii Ambala
    def find_recipes_by_pantry(
            self,
            user: User
    ) -> list[Recipe]:
        return self.recipe_service.find_recipes_by_pantry(user)
    
    #By Thanvii Ambala
    def get_recipe_by_id(
            self,
            recipe_id: int
    ) -> Optional[Recipe]:
        return self.recipe_service.get_recipe_by_id(recipe_id)
    
    #By Thanvii Ambala
    def find_recipes_by_category(
            self, 
            category: str
        ) -> list[Recipe]:
        return self.recipe_service.find_recipes_by_category(category)

    #By Thanvii Ambala
    def delete_recipe(self, recipe_id: int) -> bool:
        return self.recipe_service.delete_recipe(recipe_id)

    #By Jon Bailey
    def find_recipe(self, name: str) -> list[Recipe]:
        return self.recipe_service.find_recipe(name)
    
    #By Jon Bailey
    def add_ingredient_to_recipe(
            self,
            recipe_id: int,
            ingredient_name: str
    ) -> Recipe:
        """
        Add an ingredient to the recipe.
        """
        return self.recipe_service.add_ingredient_to_recipe(recipe_id, ingredient_name)

    #By Jon Bailey
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
    
    #By Jon Bailey
    def get_all_recipes(self) -> list[Recipe]:
        """
        Retrieve all recipes from the database.
        """
        return self.recipe_service.get_all_recipes()
    
    # ==================== Searches ====================== #
    #By Jon Bailey
    def record_search(
            self,
            query: str
    ):
        self.search_service.record_search(query )

    #By Jon Bailey
    def get_popular_searches(
            self,
            limit: int
    ) -> list[PopularSearch]:
        """
        Get the most popular searches.

        Parameters:
            limit(int): The number of items you want to return.
        
        Returns:
            list(Row(tuple(str, int))): A list of rows that contain a tuple with the name and the count of the search terms.
        """
        return self.search_service.get_popular_searches(limit = limit)
        

    #---------------- lu: STF Block | favorites container methods
    #By Lu
    def add_recipe_to_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        return self.recipe_service.add_recipe_to_favorites(user_id, recipe_id)
    
    #By Lu
    def remove_recipe_from_favorites(
            self,
            user_id: int,
            recipe_id: int
            ) -> bool:
        return self.recipe_service.remove_recipe_from_favorites(user_id, recipe_id)
    
    #By Lu
    def get_user_favorites(
            self,
            user_id: int
            ) -> list[Recipe]:
        return self.recipe_service.get_user_favorites(user_id)
    #----------
    
    #By Thanvi Ambala
    def search_recipe_by_criteria(
        self,
        include_ingredients: list[str],
        exclude_ingredients: list[str],
        category: str | None,
        dietary_requirements: list[str]
    ) -> list[Recipe]:
        return self.recipe_service.search_recipe_by_criteria(
            include_ingredients,
            exclude_ingredients,
            category,
            dietary_requirements
        )

    # ==================== DB CONTROL ==================== #

    # By Jon Bailey
    def reset_database(self):
        """
        This option will drop the entire database and rebuild columns ONLY.

        Only run this if you want to delete everything.
        """
        self.db_connect.drop_tables()
        self.db_connect.create_tables()

    # By Jon Bailey
    def close(self):
        """
        Use this to close the database connection at application
        close.
        """
        from sqlalchemy.orm import Session
        self.db_connect.shutdown()

    def migrate_database(self):
        from sqlalchemy import inspect, text

        engine = self.db_connect.engine

        if engine is None:
            raise RuntimeError("Database engine not initialized")

        inspector = inspect(engine)

        columns = [col["name"] for col in inspector.get_columns("recipes")]

        with engine.connect() as conn:

            if "published_time" not in columns:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN published_time DATETIME NULL"
                ))

            if "tags" not in columns:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN tags TEXT NULL"
                ))

            if "video" not in columns:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN video VARCHAR(500) NULL"
                ))
            
            if "category" not in columns:
                conn.execute(text(
                    "ALTER TABLE recipes ADD COLUMN category VARCHAR(255) NULL"
                ))

            conn.commit()

    
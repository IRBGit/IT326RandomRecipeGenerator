from abc import ABC, abstractmethod  # Built-in Python module for abstract classes
from .Filter import Filter           # We import Filter because it's used as a parameter type
import random
from db.database_operations import ServiceContainer

class SearchEngine(ABC):  # ABC = Abstract Base Class — acts like an <<Interface>>
    """
    Abstract interface for searching recipes.

    Any class that inherits from SearchEngine MUST implement
    every method marked with @abstractmethod below.

    Dependency on Filter (the dashed arrow in the diagram):
        Filter is passed into methods as a parameter — it is NOT
        stored as self.filter. SearchEngine just *uses* it temporarily.
    """

    def __init__(self):
        # These are the private attributes shown in the UML diagram.
        # Subclasses will connect these to real services.
        self._api_client = None          # Connects to an external recipe API
        self._service_container = None       # Accesses other services like UserService
    # Abstract methods 
    # Each method below MUST be implemented by any subclass.
    # If a subclass skips even one, Python will raise a TypeError.

    @abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> dict:
        """
        Fetch a single recipe using its unique ID.

        Args:
            recipe_id: The unique number that identifies the recipe.

        Returns:
            A recipe dictionary, or None if not found.
        """
        pass  # No body here — subclasses must write the real logic

    @abstractmethod
    def search_recipes_by_name(self, name: str) -> list:
        """
        Find recipes whose name contains the search term.

        Args:
            name: A word or phrase to look for (e.g. "pasta").

        Returns:
            A list of matching recipe dictionaries.
        """
        pass

    @abstractmethod
    def search_recipes_by_ingredients(self, ingredients: list) -> list:
        """
        Find recipes that contain ALL of the specified ingredients.

        Args:
            ingredients: A list of ingredient names (e.g. ["chicken", "garlic"]).

        Returns:
            A list of matching recipe dictionaries.
        """
        pass

    @abstractmethod
    def search_recipes_by_category(self, category: str) -> list:
        """
        Find all recipes in a given category.

        Args:
            category: Category name (e.g. "pasta", "salad", "asian").

        Returns:
            A list of matching recipe dictionaries.
        """
        pass

    @abstractmethod
    def get_random_recipes(self, count: int) -> list:
        """
        Return a random selection of recipes.

        Args:
            count: How many random recipes to return.

        Returns:
            A list of randomly chosen recipe dictionaries.
        """
        pass

    @abstractmethod
    def search_with_filter(self, recipes: list, pantry: list, recipe_filter: Filter) -> list:
        """
        Apply a Filter object to a list of recipes and return matches.

        This method is where the DEPENDENCY on Filter is shown:
            - Filter is passed in as a parameter (not stored as self.filter).
            - SearchEngine temporarily uses it, then discards it.

        Args:
            recipes:        The list of recipes to filter.
            pantry:         The user's available ingredients.
            recipe_filter:  A Filter object with the user's preferences.

        Returns:
            A filtered list of recipe dictionaries.
        """
        pass


# Concrete implementation 
# It implements every @abstractmethod so Python allows us to create instances.
class RecipeSearchEngine(SearchEngine):
    """
    A concrete (real) implementation of the SearchEngine interface.
    Uses an in-memory list of recipes so you can run this file immediately
    without any database or API setup.
    """
    def __init__(self):
        super().__init__()  # Run the parent __init__ to set up service attributes

        # Demo recipe data — replace with real DB/API calls in production
        self._recipes = []
        self._service_container = ServiceContainer()

    def get_recipe_by_id(self, recipe_id: int) -> dict | None:
        receipe = self._service_container.recipe_service.get_recipe_by_id(recipe_id)
        if receipe is None:
            return None
        return {
            "id": receipe.id,
            "name": receipe.name,
            "description": receipe.description,
            "ingredients": receipe.ingredients,
            "category": receipe.category,
            "dietary_tags": receipe.dietary_tags
        }

    def search_recipes_by_name(self, name: str) -> list:
        search_term = name.lower()
        recipes = self._service_container.recipe_service.search_recipes_by_name(search_term)
        return [
            {
                "id": recipe.id,    
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": recipe.ingredients,
                "category": recipe.category,
                "dietary_tags": recipe.dietary_tags
            }
            for recipe in recipes               
        ]

    def search_recipes_by_ingredients(self, ingredients: list) -> list:
        search_terms = [i.lower() for i in ingredients]
        results = []
        for recipe in self._recipes:
            recipe_ings = [i.lower() for i in recipe["ingredients"]]
            if all(term in recipe_ings for term in search_terms):
                results.append(recipe)
        return results

    def search_recipes_by_category(self, category: str) -> list:
        return [r for r in self._recipes if r["category"].lower() == category.lower()]
    
    #----------------------------------
        # Tolu: search recipes using simple criteria
    def search_recipes_by_criteria(self, include_ingredients: list, exclude_ingredients: list, category: str, dietary_tags: list) -> list:
        results = []

        for recipe in self._recipes:
            recipe_ingredients = []
            for ingredient in recipe["ingredients"]:
                recipe_ingredients.append(ingredient.lower())

            recipe_tags = []
            for tag in recipe.get("dietary_tags", []):
                recipe_tags.append(tag.lower())

            matches = True

            # Tolu: check ingredients the user wants included
            for ingredient in include_ingredients:
                if ingredient.lower() not in recipe_ingredients:
                    matches = False

            # Tolu: check ingredients the user does not want
            for ingredient in exclude_ingredients:
                if ingredient.lower() in recipe_ingredients:
                    matches = False

            # Tolu: check category if one was given
            if category != "":
                if recipe["category"].lower() != category.lower():
                    matches = False

            # Tolu: check dietary tags
            for tag in dietary_tags:
                if tag.lower() not in recipe_tags:
                    matches = False

            if matches:
                results.append(recipe)

        return results    

    def get_random_recipes(self, count: int) -> list:
        shuffled = self._recipes.copy()
        random.shuffle(shuffled)
        return shuffled[:count]
    
    # Alysa Solomon
    def get_random_recipe_with_filter(self, count: int, pantry: list, recipe_filter: Filter) -> list:
        shuffled = self.search_with_filter(self._recipes.copy(), pantry, recipe_filter)
        random.shuffle(shuffled)
        return shuffled[:count]

    def search_with_filter(self, recipes: list, pantry: list, recipe_filter: Filter) -> list:
        """
        Uses the Filter object temporarily to narrow down recipes.
        Notice: we do NOT do self.filter = recipe_filter — that would be
        an association. We just call recipe_filter.apply() and move on.
        This reflects the dashed dependency arrow in the UML diagram.
        """
        return recipe_filter.apply(recipes, pantry) 
    
    #Thanvi Ambala
    def offer_recipes_with_pantry(self, pantry: list) -> list:
        """
        Return recipes that can be made using ONLY the ingredients
        available in the user's pantry.
        """
        matched_recipes = []

        pantry_items = [item["ingredient"].lower() for item in pantry]

        for recipe in self._recipes:
            recipe_ingredients = [ing.lower() for ing in recipe["ingredients"]]

            if all(ingredient in pantry_items for ingredient in recipe_ingredients):
                matched_recipes.append(recipe)

        return matched_recipes
 
"""
    Author: Thanvi Ambala
"""
from abc import ABC, abstractmethod  # Built-in Python module for abstract classes
from SearchEngine.Filter import Filter            # We import Filter because it's used as a parameter type
from db.database_operations import ServiceContainer  # For real DB interactions in a full implementation
from model.recipe import Recipe  # Assuming you have a Recipe model 

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
        self.service = None              # Connects to the database repositories via ServiceContainer

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

    def __init__(self, service: ServiceContainer):
        super().__init__()  # Run the parent __init__ to set up service attributes
        self.service = service  # In a real implementation, this would connect to the DB

    def get_recipe_by_id(self, recipe_id: int) -> Recipe | None:
        recipe = self.service.get_recipe_by_id(recipe_id)
        return recipe

    def search_recipes_by_name(self, name: str) -> list | None:
        return self.service.find_recipe(name)

    def search_recipes_by_ingredients(self, ingredients: list) -> list:
        return self.service.find_recipes_by_ingredients(ingredients)

    def search_recipes_by_category(self, category: str) -> list:
        return self.service.find_recipes_by_category(category)

    def get_random_recipes(self, count: int) -> list:
        all_recipes = self.service.get_all_recipes()
        if count >= len(all_recipes):
            return all_recipes  # Return everything if count exceeds available recipes
        import random
        return random.sample(all_recipes, count)

    def offer_recipes_with_pantry(self, pantry: list) -> list:
        """
        Return recipes that can be made using ONLY the ingredients
        available in the user's pantry.

        Args:
          pantry: list of ingredient names the user currently has

        Returns:
          List of recipes the user can make
        """
        return self.service.find_recipes_by_ingredients(pantry)
        
    def search_with_filter(self, recipes: list, pantry: list, recipe_filter: Filter) -> list:
        """
        Uses the Filter object temporarily to narrow down recipes.
        Notice: we do NOT do self.filter = recipe_filter — that would be
        an association. We just call recipe_filter.apply() and move on.
        This reflects the dashed dependency arrow in the UML diagram.
        """
        if recipes is None:
            print("No recipes to filter.")
            return []
        if pantry is None:
            return recipe_filter.apply(recipes)  # If no pantry info, just apply the filter as is
        pantryrecipe = self.offer_recipes_with_pantry(pantry)
        return recipe_filter.apply(pantryrecipe) 
"""
    Author: Thanvi Ambala
"""
from abc import ABC, abstractmethod  # Built-in Python module for abstract classes
from Filter import Filter            # We import Filter because it's used as a parameter type


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
        self._db_query = None            # Runs database queries
        self._user_service = None        # Manages user accounts
        self._ingredient_service = None  # Manages ingredient data
        self._pantry_service = None      # Manages the user's pantry
        self._recipe_service = None      # Manages recipe storage/retrieval

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
        self._recipes = [
            {
                "id": 1,
                "name": "Spaghetti Bolognese",
                "category": "pasta",
                "ingredients": ["spaghetti", "ground beef", "tomato sauce", "onion"],
                "cook_time": 40,
                "calories": 550,
            },
            {
                "id": 2,
                "name": "Caesar Salad",
                "category": "salad",
                "ingredients": ["romaine lettuce", "croutons", "parmesan", "caesar dressing"],
                "cook_time": 10,
                "calories": 300,
            },
            {
                "id": 3,
                "name": "Chicken Stir-fry",
                "category": "asian",
                "ingredients": ["chicken", "broccoli", "soy sauce", "garlic"],
                "cook_time": 20,
                "calories": 400,
            },
            {
                "id": 4,
                "name": "Veggie Pasta",
                "category": "pasta",
                "ingredients": ["penne", "zucchini", "bell pepper", "olive oil"],
                "cook_time": 25,
                "calories": 380,
            },
            {
                "id": 5,
                "name": "Greek Salad",
                "category": "salad",
                "ingredients": ["cucumber", "tomato", "feta", "olives", "red onion"],
                "cook_time": 5,
                "calories": 220,
            },
        ]

    def get_recipe_by_id(self, recipe_id: int) -> dict | None:
        for recipe in self._recipes:
            if recipe["id"] == recipe_id:
                return recipe
        print(f"No recipe found with id {recipe_id}.")
        return None

    def search_recipes_by_name(self, name: str) -> list:
        name_lower = name.lower()
        return [r for r in self._recipes if name_lower in r["name"].lower()]

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

    def get_random_recipes(self, count: int) -> list:
        import random
        shuffled = self._recipes.copy()
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

    def offer_recipes_with_pantry(self, pantry: list) -> list:
        """
        Return recipes that can be made using ONLY the ingredients
        available in the user's pantry.

        Args:
          pantry: list of ingredient names the user currently has

        Returns:
          List of recipes the user can make
        """
        matched_recipes = []

        # Convert pantry to lowercase for comparison
        pantry_items = [item.lower() for item in pantry]

        for recipe in self._recipes:
            recipe_ingredients = [ing.lower() for ing in recipe["ingredients"]]

            # Check if ALL recipe ingredients exist in pantry
            if all(ingredient in pantry_items for ingredient in recipe_ingredients):
                matched_recipes.append(recipe)

        return matched_recipes

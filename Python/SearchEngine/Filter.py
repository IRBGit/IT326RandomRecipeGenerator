# filter.py
# This file contains the Filter class, which is used to filter a list of recipes
# based on user preferences like cook time, calories, and dietary restrictions.
# Tolu:
# Clean ingredient names before comparing
# Check blocked ingredients
# Only keep recipes the pantry can make

class Filter:
    """
    The Filter class stores a set of preferences/rules that can be applied
    to a list of recipes to narrow them down to what the user actually wants.
    """

    def __init__(self):
        # The minimum and maximum cook time (in minutes) allowed
        self.min_cook_time: int = 0
        self.max_cook_time: int = 9999  # default: no upper limit

        # A list of ingredients the user prefers (dietary restrictions / allowed ingredients)
        # Example: ["gluten-free", "vegan"]
        self.dietary_restrictions: list = []

        # The minimum and maximum calories allowed per recipe
        self.min_calories: int = 0
        self.max_calories: int = 9999  # default: no upper limit

        # Ingredients the user wants to completely avoid
        # Example: ["peanuts", "shellfish"]
        self.blocked_ingredients: list = []

        # If True, only return recipes that can be made using pantry items the user has
        self.use_pantry_only: bool = False

    def validate(self) -> bool:
        """
        Checks if the filter settings make sense before using them.
        For example, min cook time should not be greater than max cook time.

        Returns:
            True if everything is valid, False if something is wrong.
        """
        if self.min_cook_time > self.max_cook_time:
            print("Error: min_cook_time cannot be greater than max_cook_time.")
            return False

        if self.min_calories > self.max_calories:
            print("Error: min_calories cannot be greater than max_calories.")
            return False

        if self.min_cook_time < 0 or self.min_calories < 0:
            print("Error: Time and calorie values cannot be negative.")
            return False

        return True  # All checks passed!
    
    # Tolu: clean one ingredient name
    def _clean_name(self, value):
        return str(value).strip().lower()

    # Tolu: added to clean a whole ingredient list
    def _clean_list(self, values):
        cleaned = []
        for value in values:
            cleaned.append(self._clean_name(value))
        return cleaned

    def matches(self, recipe: dict, pantry: list) -> bool:
        """
        Checks whether a single recipe passes all of the filter rules.

        Args:
            recipe: A dictionary representing one recipe.
                    Expected keys: 'cook_time', 'calories', 'ingredients'
            pantry: A list of ingredient names the user currently has at home.

        Returns:
            True if the recipe matches all filter rules, False otherwise.
        """
        # Tolu: Check cook time range
        cook_time = recipe.get("cook_time")

        if cook_time is None:
            return False

        if not (self.min_cook_time <= cook_time <= self.max_cook_time):
            return False
            
        # Check calorie range
        calories = recipe.get("calories", 0)
        if not (self.min_calories <= calories <= self.max_calories):
            return False

        # Check that none of the recipe's ingredients are blocked
        recipe_ingredients = self._clean_list(recipe.get("ingredients", []))
        pantry_ingredients = self._clean_list(pantry)
        blocked_ingredients = self._clean_list(self.blocked_ingredients)

        
        for ingredient in recipe_ingredients:
            if ingredient in blocked_ingredients:
                return False

        # If use_pantry_only is True, every ingredient must be in the pantry
        if self.use_pantry_only:
            for ingredient in recipe_ingredients:
                if ingredient not in pantry_ingredients:
                    return False # Missing an ingredient from the pantry

        return True  # Recipe passed all checks!

    def apply(self, recipes: list, pantry: list) -> list:
        """
        Filters a whole list of recipes, returning only those that match
        the current filter settings.

        Args:
            recipes: A list of recipe dictionaries.
            pantry: A list of ingredient names the user has at home.

        Returns:
            A new list containing only the recipes that passed the filter.
        """
        # First, make sure the filter settings are valid
        if not self.validate():
            print("Filter settings are invalid. Returning empty list.")
            return []

        # Go through each recipe and keep only those that match
        matching_recipes = []
        for recipe in recipes:
            if self.matches(recipe, pantry):
                matching_recipes.append(recipe)

        return matching_recipes


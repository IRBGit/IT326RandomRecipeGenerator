"""
    Author: Thanvi Ambala
"""
class Filter:
    """
    The Filter class stores a set of preferences/rules that can be applied
    to a list of recipes to narrow them down to what the user actually wants.
    """

    def __init__(self):
        # A list of ingredients the user prefers (dietary restrictions / allowed ingredients)
        # Example: ["gluten-free", "vegan"]
        self.dietary_restrictions: list = []

        # Ingredients the user wants to completely avoid
        # Example: ["peanuts", "shellfish"]
        self.blocked_ingredients: list = []

        # If True, only return recipes that can be made using pantry items the user has
        self.use_pantry_only: bool = False
    
    # Tolu: clean one ingredient name
    def _clean_name(self, value):
        return str(value).strip().lower()

    # Tolu: added to clean a whole ingredient list
    def _clean_list(self, values):
        cleaned = []
        for value in values:
            cleaned.append(self._clean_name(value))
        return cleaned

    def matches(self, recipe: dict) -> bool:
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
        # Check that none of the recipe's ingredients are blocked
        recipe_ingredients = self._clean_list(recipe.get("ingredients", []))
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

    def apply(self, recipes: list) -> list:
        """
        Filters a whole list of recipes, returning only those that match
        the current filter settings.

        Args:
            recipes: A list of recipe dictionaries.
            pantry: A list of ingredient names the user has at home.

        Returns:
            A new list containing only the recipes that passed the filter.
        """
        # Go through each recipe and keep only those that match
        matching_recipes = []
        for recipe in recipes:
            if self.matches(recipe):  # Pass an empty pantry list
                matching_recipes.append(recipe)

        return matching_recipes



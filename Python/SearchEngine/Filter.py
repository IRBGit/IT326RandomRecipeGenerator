"""
    Author: Thanvi Ambala
"""
from model.recipe import Recipe

class Filter:
    """
    The Filter class stores rules that can be applied to recipes.
    It helps return only the recipes that match what the user wants.
    """

    def __init__(self):
        self.dietary_restrictions: list = []
        self.blocked_ingredients: list = []
        self.use_pantry_only: bool = False

    def _clean_name(self, value):
        return str(value).strip().lower()

    def _clean_list(self, values):
        cleaned = []

        if values is None:
            return cleaned

        for value in values:
            cleaned.append(self._clean_name(value))

        return cleaned

    def _get_recipe_ingredient_names(self, recipe: Recipe) -> list:
        """
        Gets all ingredient names from a recipe.
        """
        ingredient_names = []

        for recipe_ingredient in recipe._ingredients.values():
            ingredient = recipe_ingredient.ingredient

            if ingredient is not None:
                ingredient_names.append(self._clean_name(ingredient.name))

        return ingredient_names

    def matches(self, recipe: Recipe) -> bool:
        """
        Checks if one recipe passes the filter rules.
        """
        recipe_ingredient_names = self._get_recipe_ingredient_names(recipe)
        recipe_tags = self._clean_list(recipe.tags)

        cleaned_blocked = self._clean_list(self.blocked_ingredients)
        cleaned_dietary = self._clean_list(self.dietary_restrictions)

        # Rule 1: blocked ingredients should NOT be in the recipe
        for blocked in cleaned_blocked:
            if blocked in recipe_ingredient_names:
                return False

        # Rule 2: dietary restrictions should match recipe tags
        for restriction in cleaned_dietary:
            if restriction not in recipe_tags:
                return False

        return True

    def apply(self, recipes: list) -> list:
        """
        Filters a list of recipes.
        """
        filtered_recipes = []

        for recipe in recipes:
            if self.matches(recipe):
                filtered_recipes.append(recipe)

        return filtered_recipes
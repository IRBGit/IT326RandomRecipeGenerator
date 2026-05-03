"""
Author - Test Suite
Test filtering recipes by current ingredients (pantry-based search)
"""

import unittest
from db.database_operations import ServiceContainer
from sqlalchemy.exc import OperationalError


class TestFilterByCurrentIngredients(unittest.TestCase):
    def setUp(self):
        try:
            self.service = ServiceContainer()
            self.user = self.service.create_user("pantry_test@example.com", "StrongPass1!")
            self.created_recipes = []
        except OperationalError as e:
            if "DPY-6005" in str(e) or "cannot connect" in str(e):
                self.skipTest("Database connection unavailable (requires ISU VPN)")
            raise

    def tearDown(self):
        for recipe in self.created_recipes:
            try:
                self.service.delete_recipe(recipe.id)
            except Exception:
                pass
        try:
            self.service.delete_user(self.user)
        except Exception:
            pass

    def test_recipes_with_all_pantry_ingredients(self):
        """Recipes using only pantry ingredients are found"""
        flour = self.service.add_ingredient("flour")
        sugar = self.service.add_ingredient("sugar")
        self.service.add_to_pantry(self.user, flour)
        self.service.add_to_pantry(self.user, sugar)

        recipe = self.service.add_recipe("Simple Cake", ["Bake"], [{"name": "flour"}, {"name": "sugar"}])
        self.created_recipes.append(recipe)

        results = self.service.find_recipes_by_pantry(self.user)
        self.assertTrue(any(r.id == recipe.id for r in results))

    def test_recipes_missing_ingredients_excluded(self):
        """Recipes with missing ingredients are excluded"""
        flour = self.service.add_ingredient("flour")
        self.service.add_to_pantry(self.user, flour)

        recipe = self.service.add_recipe(
            "Cake", 
            ["Bake"], 
            [{"name": "flour"}, {"name": "eggs"}]  # eggs not in pantry
        )
        self.created_recipes.append(recipe)

        results = self.service.find_recipes_by_pantry(self.user)
        self.assertFalse(any(r.id == recipe.id for r in results))

    def test_empty_pantry_returns_no_recipes(self):
        """Empty pantry returns no matching recipes"""
        flour = self.service.add_ingredient("flour")
        recipe = self.service.add_recipe("Bread", ["Bake"], [{"name": "flour"}])
        self.created_recipes.append(recipe)

        results = self.service.find_recipes_by_pantry(self.user)
        self.assertFalse(any(r.id == recipe.id for r in results))


if __name__ == '__main__':
    unittest.main()

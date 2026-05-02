"""
Author - Thanvi Ambala
"""
import unittest
from db.database_operations import ServiceContainer
from SearchEngine import SearchEngine

class TestSearchRecipeByName(unittest.TestCase):
    def setUp(self):
        self.recipe_list = []
        self.service_container = ServiceContainer()
        self.search_engine = SearchEngine.RecipeSearchEngine(self.service_container) 

    def test_search_recipe_by_name_exact_match(self):
        self.service_container.add_recipe("Spaghetti Bolognese", ["Boil Pasta", "Cook Sauce", "Combine Ingredients"] , ["pasta", "beef", "tomato"])
        results = self.search_engine.search_recipes_by_name("Spaghetti Bolognese")
        self.assertIsNotNone(results)
        self.assertTrue(len(results) >= 1)
        self.assertTrue(any(recipe.get_name() == "Spaghetti Bolognese" for recipe in results), "Exact match not found in results")

    def test_search_recipe_by_name_partial_match(self):
        self.service_container.add_recipe("Chicken Alfredo", ["Cook Chicken", "Make Alfredo Sauce", "Combine Ingredients"] , ["chicken", "pasta", "cream"])
        results = self.search_engine.search_recipes_by_name("Alfredo")
        self.assertIsNotNone(results)
        self.assertTrue(len(results) > 1)
        self.assertTrue(any("Alfredo" in recipe.get_name() for recipe in results), "Partial match not found in results")

    def test_search_recipe_by_name_no_match(self):
        results = self.search_engine.search_recipes_by_name("tacswrtwzi")
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 0, "Expected no matches, but some were found")

    def test_search_recipe_by_name_case_insensitive(self):
        self.service_container.add_recipe("Caesar Salad", ["Chop Lettuce", "Make Dressing", "Combine Ingredients"] , ["lettuce", "croutons", "parmesan"])
        results = self.search_engine.search_recipes_by_name("caesar salad")
        self.assertIsNotNone(results)
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any(recipe.get_name().lower() == "caesar salad" for recipe in results), "Case-insensitive match not found in results")
        
    def tearDown(self) -> None:
        for recipe in self.recipe_list:
            self.service_container.delete_recipe(recipe.get_id())
        

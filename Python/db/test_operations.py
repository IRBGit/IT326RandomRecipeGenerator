"""
Test Driver for Database + Service Layer
Author: Jon Bailey
"""

from db.db_connect import DBConnect
from db.db_query import DBQuery

from model import Ingredient, User, Recipe, PantryItem, recipe_ingredients, user_favorites

from db.database_operations import (
    UserService,
    IngredientService,
    PantryService,
    RecipeService
)

def main():
    print("=== STARTING TEST DRIVER ===")

    

    # -------------------- Setup -------------------- #
    db_connect = DBConnect()
    db_connect.connect()

    # Optional reset
    db_connect.drop_tables()
    db_connect.create_tables()

    db_query = DBQuery(db_connect)

    user_service = UserService(db_query)
    ingredient_service = IngredientService(db_query)
    pantry_service = PantryService(db_query)
    recipe_service = RecipeService(db_query)

    # -------------------- Create Users -------------------- #
    print("\n--- Creating Users ---")
    user = user_service.create_user("test@example.com", "Password123!")
    print("User:", user)

    # -------------------- Create Ingredients -------------------- #
    print("\n--- Creating Ingredients ---")
    flour = ingredient_service.add_ingredient("Flour")
    sugar = ingredient_service.add_ingredient("Sugar")
    eggs = ingredient_service.add_ingredient("Eggs")

    print(flour, sugar, eggs)

    # -------------------- Pantry Tests -------------------- #
    print("\n--- Pantry Operations ---")

    pantry_service.add_ingredient_to_pantry(user, flour, 2, "cups")
    pantry_service.add_ingredient_to_pantry(user, sugar, 1, "cup")

    assert user is not None
    assert flour is not None
    assert sugar is not None
    assert eggs is not None

    print("Pantry after adding:")
    print(user.get_pantry())

    pantry_service.update_pantry_item(user, flour, 3, "cups")

    print("Pantry after update:")
    print(user.get_pantry())

    pantry_service.remove_ingredient_from_pantry(user, sugar)

    print("Pantry after removal:")
    print(user.get_pantry())

    # -------------------- Recipe Tests -------------------- #
    print("\n--- Recipe Operations ---")

    recipe = recipe_service.add_recipe(
        name="Pancakes",
        instructions=[
            "Mix ingredients",
            "Cook on skillet"
        ],
        ingredients=[flour, eggs]
    )
    assert recipe is not None

    print("Recipe:", recipe)
    print("Recipe ingredients:", recipe.ingredients)

    # -------------------- Query Test -------------------- #
    print("\n--- Query Test ---")
    found_user = user_service.get_user_by_email("test@example.com")
    print("Found user:", found_user)

    found_recipe = recipe_service.find_recipe("Pancakes")
    print("Found recipe:", found_recipe)

    # -------------------- Delete Test -------------------- #
    print("\n--- Delete Test ---")

    recipe_deleted = recipe_service.delete_recipe(recipe)
    print("Recipe deleted:", recipe_deleted)

    user_deleted = user_service.delete_user(user)
    print("User deleted:", user_deleted)

    # -------------------- Cleanup -------------------- #
    db_query.close()
    db_connect.close_session()

    print("\n=== TEST DRIVER COMPLETE ===")


if __name__ == "__main__":
    main()
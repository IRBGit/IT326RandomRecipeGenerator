from db.database_operations import ServiceContainer as container
from model import User, Recipe, Ingredient

def driver():
    user: User = container.get_user_by_email("jrbail1@ilstu.edu")
    recipe: Recipe = container.add_recipe("Cake", ["Set up oven", "Bake Cake"])

    ing: Ingredient = container.find_ingredient("Flour")
    container.add_ingredient_to_recipe(ing.idi, ing.name)

if __name__ == "__main__":
    try:
        driver()
    finally:
        container.close()

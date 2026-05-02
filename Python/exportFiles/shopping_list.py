from db.database_operations import ServiceContainer
from model import Recipe, User


def build_shopping_list(service: ServiceContainer, user: User, recipe: Recipe) -> list[dict]:
    pantry_items = service.get_all_pantry_items(user) or []
    pantry_by_id = {
        item["ingredient_id"]: item
        for item in pantry_items
    }
    pantry_by_name = {
        item["ingredient_name"].strip().lower(): item
        for item in pantry_items
    }

    shopping_list = []

    for recipe_ingredient in recipe._ingredients.values():
        ingredient = recipe_ingredient.ingredient
        pantry_item = pantry_by_id.get(ingredient.id)

        if pantry_item is None:
            pantry_item = pantry_by_name.get(ingredient.name.strip().lower())

        required_quantity = recipe_ingredient.quantity
        required_unit = (recipe_ingredient.unit or "").strip().lower()

        if pantry_item is None:
            shopping_list.append(
                {
                    "name": ingredient.name,
                    "quantity": required_quantity,
                    "unit": recipe_ingredient.unit or "",
                }
            )
            continue

        pantry_quantity = pantry_item.get("quantity")
        pantry_unit = (pantry_item.get("unit") or "").strip().lower()

        if (
            required_quantity is not None
            and pantry_quantity is not None
            and required_unit == pantry_unit
        ):
            remaining_quantity = required_quantity - pantry_quantity
            if remaining_quantity > 0:
                shopping_list.append(
                    {
                        "name": ingredient.name,
                        "quantity": remaining_quantity,
                        "unit": recipe_ingredient.unit or "",
                    }
                )

    return shopping_list


def print_shopping_list(recipe: Recipe, shopping_list: list[dict]):
    print(f"\nShopping List for {recipe.get_name()}")
    print("--------------------")

    if not shopping_list:
        print("You already have everything needed in your pantry.")
        return

    for item in shopping_list:
        quantity = item.get("quantity")
        unit = item.get("unit") or ""
        name = item.get("name", "Unknown")

        if quantity is None:
            line = name
        elif unit == "":
            line = f"{quantity} {name}"
        else:
            line = f"{quantity} {unit} {name}"

        print(f"- {line}")
import json
import os
from db.database_operations import ServiceContainer

def import_recipes_from_json(file_path):
    container = ServiceContainer()
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        recipes_to_import = data.get("Recipe", [])
        print(f"--- Found {len(recipes_to_import)} recipes to import ---")

        for entry in recipes_to_import:
            name = entry.get("recipeName")
            
            # 1. Process Instructions: Split by \n and clean up whitespace
            raw_steps = entry.get("steps", "")
            instructions_list = [step.strip() for step in raw_steps.split('\n') if step.strip()]
            
            # 2. Process Ingredients: Extract names and ignore quantities
            ingredient_data = entry.get("ingredients", [])
            ingredient_names = [ing.get("ingredientName") for ing in ingredient_data if ing.get("ingredientName")]
            
            try:
                # 3. Use ServiceContainer to add the recipe
                # Note: add_recipe takes a list of instruction strings and a list of ingredient names
                recipe = container.recipe_service.add_recipe(
                    name=name,
                    instructions=instructions_list,
                    ingredients=ingredient_names
                )
                if recipe:
                    print(f" [SUCCESS] Imported: {name} with {len(ingredient_names)} ingredients.")
            except Exception as e:
                print(f" [ERROR] Failed to import '{name}': {e}")

    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        container.close()

if __name__ == "__main__":
    # Ensure this matches your JSON filename
    import_recipes_from_json('Sample_Recipe.json')
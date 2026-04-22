import json
import os
from db.database_operations import ServiceContainer
import datetime

def import_recipes_from_json(file_path):
    container = ServiceContainer()
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        recipes_to_import = data.get("meals", [])
        print(f"--- Found {len(recipes_to_import)} recipes to import ---")
        for entry in recipes_to_import:
            name = entry.get("strMeal")
            
            # 1. Process Instructions: Split by \n and clean up whitespace
            raw_steps = entry.get("strInstructions", "")
            instructions_list = [step.strip() for step in raw_steps.split('\n') if step.strip()]
            
            # empties the ingredient names from previous entries
            ingredient_names = []
            quantity_list = []

            # adds all the ingredients to Recipe database
            # TODO: add all ingredient quantites when recipe ing quanity added to database. 
            for i in range(1,21):
                # ingredients
                ing_item = entry.get("strIngredient"+str(i))
                # quantity
                qua_item = entry.get("strMeasure"+str(i))
                if ing_item != "":
                    ingredient_names.append(ing_item)
                    quantity_list.append(qua_item)
                    
            time_stamp_str = entry.get("dateModified")
            # 2025-11-16 01:49:18
            if (time_stamp_str != None):
                time_stamp = datetime.datetime.strptime(time_stamp_str,"%Y-%m-%d %H:%M:%S")

            print("Variables Created")

            try:
                # 3. Use ServiceContainer to add the recipe
                # Note: add_recipe takes a list of instruction strings and a list of ingredient names
                recipe = container.recipe_service.add_recipe(
                    name=name,
                    instructions=instructions_list,
                    ingredients=ingredient_names,
                    pub_time=time_stamp
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
        pass

if __name__ == "__main__":
    # Ensure this matches your JSON filename
    import_recipes_from_json('Python\\theMealDB_A.json')
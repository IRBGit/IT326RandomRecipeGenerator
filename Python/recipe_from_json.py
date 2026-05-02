import json
import os
from db.database_operations import ServiceContainer
import datetime

def parse_fraction(value):
    parts = value.split("/")

    if len(parts) != 2:
        return None

    try:
        top = float(parts[0])
        bottom = float(parts[1])

        if bottom == 0:
            return None

        return top / bottom
    except ValueError:
        return None

def normalize_unit(unit_text):
    unit_text = unit_text.strip().lower()

    unit_map = {
        "cup": "cup",
        "cups": "cups",
        "tbsp": "tbsp",
        "tblsp": "tbsp",
        "tbls": "tbsp",
        "tablespoon": "tablespoon",
        "tablespoons": "tablespoons",
        "tsp": "tsp",
        "teaspoon": "teaspoon",
        "teaspoons": "teaspoons",
        "oz": "oz",
        "ounce": "ounce",
        "ounces": "ounces",
        "lb": "lb",
        "lbs": "lb",
        "pound": "pound",
        "pounds": "pounds",
        "ml": "ml",
        "l": "l",
        "g": "g",
        "kg": "kg",
        "clove": "cloves",
        "cloves": "cloves"
    }

    if unit_text in unit_map:
        return unit_map[unit_text]

    return ""


def parse_measure_text(measure_text):
    if not measure_text:
        return None, ""

    measure_text = measure_text.strip()

    if measure_text == "":
        return None, ""

    measure_text = measure_text.replace(",", " ")
    parts = measure_text.split()

    if len(parts) == 0:
        return None, ""

    amount = None
    unit = ""

    # case: 1 1/2 cups
    if len(parts) >= 2:
        try:
            whole = float(parts[0])
            fraction = parse_fraction(parts[1])

            if fraction is not None:
                amount = whole + fraction
                parts = parts[2:]
        except ValueError:
            pass

    # case: 2 cups or 1.5 cups
    if amount is None:
        try:
            amount = float(parts[0])
            parts = parts[1:]
        except ValueError:
            pass

    # case: 1/2 cup
    if amount is None:
        fraction = parse_fraction(parts[0])

        if fraction is not None:
            amount = fraction
            parts = parts[1:]

    # case: 225g or 400ml
    if amount is None:
        first = parts[0]
        number_text = ""
        unit_text = ""

        for char in first:
            if char.isdigit() or char == ".":
                number_text += char
            else:
                unit_text += char

        if number_text != "" and unit_text != "":
            try:
                amount = float(number_text)
                unit = normalize_unit(unit_text)
                return amount, unit
            except ValueError:
                pass

    if amount is None:
        return None, ""

    ignore_words = {
        "small", "medium", "large", "finely", "roughly",
        "chopped", "sliced", "diced", "to", "serve",
        "for", "garnish", "extra", "plus", "stick"
    }

    for word in parts:
        clean_word = word.strip().lower()

        if clean_word in ignore_words:
            continue

        unit = normalize_unit(clean_word)

        if unit != "":
            break

    return amount, unit

def import_recipes_from_json(file_path):
    container = ServiceContainer()
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return


    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        recipes_to_import = data.get("meals") or []
        print(f"--- Found {len(recipes_to_import)} recipes to import ---")
        for entry in recipes_to_import:
            name = entry.get("strMeal")
            
            # 1. Process Instructions: Split by \n and clean up whitespace
            raw_steps = entry.get("strInstructions", "")
            instructions_list = [step.strip() for step in raw_steps.split('\n') if step.strip()]
            
            # empties the ingredient names from previous entries
            ingredient_data = []

            # adds all the ingredients to Recipe database
            for i in range(1, 21):
                ing_item = entry.get("strIngredient" + str(i))
                qua_item = entry.get("strMeasure" + str(i))

                ing_item = (ing_item or "").strip()
                qua_item = (qua_item or "").strip()

                if ing_item != "":
                    quantity, unit = parse_measure_text(qua_item)

                    if quantity is None:
                        unit = ""

                    ingredient_data.append({
                        "name": ing_item,
                        "quantity": quantity,
                        "unit": unit
                    })

            time_stamp = None    
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
                    ingredients=ingredient_data,
                    pub_time=time_stamp
                )
                if recipe:
                    print(f" [SUCCESS] Imported: {name} with {len(ingredient_data)} ingredients.")
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

    # import_recipes_from_json('Python\\theMealDB_A.json')
    recipe_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","Z","0","1","2","3","4","5","6","7","8","9"]
    for letter in recipe_list:
        import_recipes_from_json(os.path.join("JSON_Recipes", f"{letter}_recipes.json"))
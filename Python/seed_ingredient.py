import os
import sys

# 1. Adjust path to find your db and model packages if necessary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database_operations import ServiceContainer

def seed_ingredients_from_file(file_path: str):
    # Initialize the container
    container = ServiceContainer()
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"--- Starting Ingredient Seed from {file_path} ---")
    
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Remove whitespace/newlines
                ingredient_name = line.strip()
                
                # Skip empty lines
                if not ingredient_name:
                    continue
                
                try:
                    # Use the ServiceContainer to add the ingredient
                    # This method handles the check to see if it already exists
                    result = container.add_ingredient(ingredient_name)
                    if result:
                        print(f" [SUCCESS] Added: {ingredient_name}")
                        count += 1
                except Exception as e:
                    print(f" [ERROR] Could not add '{ingredient_name}': {e}")
                    
        print(f"--- Seed Complete! Total added/verified: {count} ---")
        
    except Exception as e:
        print(f"Failed to read file: {e}")
    finally:
        # Properly close the DB connection
        container.close()

if __name__ == "__main__":
    # Ensure this matches the relative path to your file
    seed_ingredients_from_file('ingredients-list.txt')
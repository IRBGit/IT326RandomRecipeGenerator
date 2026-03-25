import random
from db.database_operations import ServiceContainer

def seed_user_pantries():
    container = ServiceContainer()
    
    # 1. Fetch all users and ingredients
    # Note: These service methods return ORM objects
    #all_recipes = container.get_all_recipes() # Just to ensure DB is connected
    users = [container.get_user_by_id(i) for i in range(1, 11)]
    
    # We'll use a raw query or add a service method to get all ingredients
    all_ingredients = [container.get_ingredient_by_id(i) for i in range(1,98)]

    if not users:
        print("Error: Could not find users in the database.")
        return
    
    if not all_ingredients:
        print("Error: Could not find ingredients")
        return

    print(f"--- Seeding pantries for {len(users)} users ---")

    units = ["pkg", "cups", "oz", "lbs", "grams", "items"]

    for user in users:
        if not user: continue
        
        # Pick 5 to 10 random ingredients for this user
        num_to_add = random.randint(5, 10)
        to_add = random.sample(all_ingredients, num_to_add)
        
        for ing in to_add:
            qty = random.randint(1, 5)
            unit = random.choice(units)
            
            try:
                container.add_to_pantry(user, ing, quantity=qty, unit=unit)
                print(f" [ADDED] {user.email}: {qty} {unit} of {ing.name}")
            except Exception as e:
                print(f" [FAILED] {user.email} -> {ing.name}: {e}")

    print("--- Pantry Seeding Complete ---")
    container.close()

if __name__ == "__main__":
    seed_user_pantries()
import os
from dotenv import load_dotenv
import pathlib
from db.database_operations import ServiceContainer
from model import Recipe, User
from SearchEngine import SearchEngine, Filter, Rank
from typing import List
from datetime import datetime
from model.conversions import format_converted_amount

load_dotenv()
# By Jon Bailey
def print_pantry(service: ServiceContainer, user: User):
    items = service.get_all_pantry_items(user)

    if not items:
        print("Your pantry is empty.")
        return
    
    print("\n--- Pantry ---")
    for item in items:
        print(
            f"{item['index'] }"
            f"{item['ingredient_name']} "
            f"({item['quantity'] or 'N/A/'} {item['unit'] or ''})"
        )

    return items
#------lu:
def format_recipe_ingredient(recipe_ingredient, system):
    # get saved values
    quantity = recipe_ingredient.quantity
    unit = recipe_ingredient.unit or ""
    name = recipe_ingredient.ingredient.name

    # show normal ingredient text
    if system == "original":
        if quantity is None:
            return name
        if unit == "":
            return str(quantity) + " " + name
        return str(quantity) + " " + unit + " " + name

    # if no quantity, keep original
    if quantity is None:
        return name

    # if no unit, keep original
    if unit == "":
        return str(quantity) + " " + name

    converted = format_converted_amount(quantity, unit, system)

    # if conversion fails, keep original
    if converted == "Unit not supported":
        return str(quantity) + " " + unit + " " + name

    if converted == "System not supported":
        return str(quantity) + " " + unit + " " + name

    return converted + " " + name


def print_recipe_details(recipe_data, system):
    print("\n--------------------")
    print("Recipe:", recipe_data["name"])
    print("--------------------")

    print("\nIngredients:")
    for item in recipe_data["ingredients"]:

        quantity = item["quantity"]
        unit = item["unit"]
        name = item["name"]

        if system == "original":
            if quantity is None:
                ingredient_line = name
            elif unit == "":
                ingredient_line = str(quantity) + " " + name
            else:
                ingredient_line = str(quantity) + " " + unit + " " + name
        else:
            if quantity is None:
                ingredient_line = name
            elif unit == "":
                ingredient_line = str(quantity) + " " + name
            else:
                converted = format_converted_amount(quantity, unit, system)

                if converted == "Unit not supported" or converted == "System not supported":
                    ingredient_line = str(quantity) + " " + unit + " " + name
                else:
                    ingredient_line = converted + " " + name

        print("- " + ingredient_line)

    print("\nInstructions:")
    for i, step in enumerate(recipe_data["instructions"], start=1):
        print(str(i) + ". " + step)


def view_recipe_results(recipe_list, service):
    if recipe_list is None or recipe_list == []:
        print("No Recipes Found")
        return

    print("\nRecipes Found:")
    for i, recipe in enumerate(recipe_list, start=1):
        print(str(i) + ": " + recipe.name)

    try:
        choice = int(input("Select a recipe number to view: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice < 1 or choice > len(recipe_list):
        print("Invalid selection.")
        return

    recipe = recipe_list[choice - 1]

    recipe_data = service.get_recipe_display_data(recipe.id)

    if recipe_data is None:
        print("Could not load recipe details.")
        return

    print("\nMeasurement Options:")
    print("1: Original")
    print("2: Metric")
    print("3: Imperial")

    system_choice = input("Select your choice: ").strip()

    if system_choice == "2":
        system = "metric"
    elif system_choice == "3":
        system = "imperial"
    else:
        system = "original"

    print_recipe_details(recipe_data, system)
#-----------conv flow

def add_pantry_item(service: ServiceContainer, user: User):
    name = input("Ingredient name: ")

    ingredient = service.find_ingredient(name)
    if not ingredient:
        ingredient = service.add_ingredient(name)

    quantity = input("Quantity (optional): ")
    unit = input("Unit (Optional): ")

    quantity = float(quantity) if quantity.strip() else None
    unit  = unit if unit.strip() else None

    try:
        service.add_to_pantry(
            user, ingredient, quantity, unit
        )
    except:
        print("User not found")

def delete_pantry_item(service: ServiceContainer, user: User):
    items = print_pantry(service, user)

    try:
        index = int(input("Select item number to delete: "))
    except ValueError:
        print("Invalid input")
        return
    
    if items is not None:
        if index < 0 or index >= len(items):
            print("Invaldi Selection")
            return
    
        ingredient = service.get_ingredient_by_id(items[index]['ingredient_id'])

        service.remove_from_pantry(user, ingredient)
    
def update_pantry_item(service: ServiceContainer, user: User):
    items = print_pantry(service, user)

    try:
        index = int(input("Select item number to update: "))
    except ValueError:
        print("Invalid input.")
        return

# By Jon Bailey
def add_note_to_recipe(service: ServiceContainer, user: User, recipe: Recipe):
    try:
        note = input(f"Please enter the note you want to add to {recipe.name}: ").strip()

        if not note:
            print("Note cannot be empty.")
            return
        
        updated_notes = service.add_personal_note(user, recipe, note)

        print("Note added successfully")
    except ValueError:
        print("Invalid input")
    except Exception as e:
        print(f"Error adding note: {e}")

# By Jon Bailey
def delete_note_from_recipe(service: ServiceContainer,user: User):
    try:
        indexed_notes = service.get_all_user_notes(user)

        if not indexed_notes:
            return
        
        #Display numbered list
        print("\nYour Notes:")
        for i, (recipe, note) in enumerate(indexed_notes, start = 1):
            print(f"{i}.{recipe.name}: {note}")
        
        
        choice = int(input("Select the number of the note to delete: "))

        if choice <1 or choice > len(indexed_notes):
            print("Invalid selection.")
            return
        
        recipe, note = indexed_notes[choice - 1]

        updated_notes = service.delete_personal_note(user, recipe, note)

        print("Note deleted successfully.")
    except ValueError:
        print("Invlaid input")
    except Exception as e:
        print(f"Error deleting note: {e}")

# By Jon Bailey    
def update_note(service, user):
    try:
        # Get all notes (flattened list)
        notes = service.get_all_user_notes(user.id)

        if not notes:
            print("No notes found.")
            return
        
        #Display numbered list
        print("\nYour Notes:")
        for i, (recipe, note) in enumerate(notes, start = 1):
            print(f"{i}.{recipe.name}: {note}")
        
        # Select note to update
        choice = int(input("\nSelect note to update: "))

        if choice < 1 or choice > len(notes):
            print("Invalid selection")
            return
        
        recipe, old_note = notes[choice - 1]

        # Get new note
        new_note = input("Enter updated note: ").strip()

        if not new_note:
            print("Note cannot be empty.")
            return
        
        updated_notes = service.update_note(user, recipe, old_note, new_note)

        print("\nNote updated successfully.")
        print(f"Updated notes for '{recipe.name} : ")
        for n in updated_notes:
            print(f"- {n}")
    except ValueError:
        print("Invalid input.")
    except Exception as e:
        print(f"Error updating note: {e}")

# By Thanvii Ambala
def login(service: ServiceContainer, username, password):
    """
    Authenticates user using database.
    Returns (success, message, user)
    """

    if not username or not password:
        return False, "Username and password cannot be empty", None

    try:
        user = service.authenticate_user(username, password)

        if user:
            return True, "Login successful", user
        else:
            return False, "Invalid username or password", None

    except Exception as e:
        return False, f"Error during login: {e}", None
    
# By Thanvii Ambala
def logout():
    """
    Logs the user out.
    """
    return True, "Logged out successfully", None

# By Thanvii Ambala and Alysa Solomon
def loginHelper(service):
    email = input("Enter email: ")
    password = input("Enter password: ")

    success, message, user = login(service, email, password)
    print(message)

    if success:
        print("You are now logged in!")
        return user

    return None

# By Thanvii Ambala
def logoutHelper():
    print(logout())
    return None

# By Alysa Solomon
#TODO: NOT DONE
def retrieve_recipe(recipes: List[Recipe]):
    getting_recipe = True

# By Alysa Solomon
def get_ingredients(outputString: str):
    count = 0
    gettingCount = True
    while gettingCount:
        try:
            count = int(input(outputString))
            gettingCount = False
        except ValueError:
            print("Please input a valid input.")
            pass
        pass

    ing_list = []
    print("Please input name of ingredients, one at a time.")
    for _ in range(count):
        ing_list.append(input())
    return ing_list

# By Alysa Solomon
def get_category():
    category_list = ["Beef",
                     "Breakfast",
                     "Chicken",
                     "Dessert", 
                     "Goat",
                     "Lamb", 
                     "Miscellaneous",
                     "Pasta"
                     "Pork",
                     "Seafood"
                     "Side",
                     "Starter",
                     "Vegan",
                     "Vegetarian"]
    while True:
        print("The valid categories are:")
        for i in range(len(category_list)):
            print(f"{i}: "+category_list[i])
        try:
            print(str(len(category_list)+1)+": No Desired Category")
            chosed_option = input()
            chosed_option = int(chosed_option)
            if chosed_option == (len(category_list)+1):
                return ""
            if chosed_option > (len(category_list)+1):
                input("Invalid Option. Press Enter to Continue")
            else:
                return category_list[chosed_option]
        except ValueError:
            print("Please input a valid input.")
            pass


# By Alysa Solomon
def get_dietary():
    #TODO: I don't know if this is correct
    category_list = ["Algerian","American","Argentinian","Australian","British","Canadian","Chinese","Croatian","Dutch",
                     "Egyptian","Filipino","French","Greek","Indian","Irish","Italian","Jamaican","Japanese","Kenyan",
                     "Malaysian","Mexican","Moroccan","Norwegian","Polish","Portuguese","Russian","Saudi Arabian","Slovakian",
                     "Spanish","Syrian","Thai","Tunisian","Turkish","Ukrainian","Uruguayan","Venezulan","Vietnamese"]
    while True:
        print("Valid Categories:")
        for i in range(len(category_list)):
            print(f"{i}: "+category_list[i])
        try:
            print(str(len(category_list)+1)+": No Desired Category")
            chosed_option = input()
            chosed_option = int(chosed_option)
            if chosed_option == (len(category_list)+1):
                return ""
            if chosed_option > (len(category_list)+1):
                input("Invalid Option. Press Enter to Continue")
            else:
                return category_list[chosed_option]
        except ValueError:
            print("Please input a valid input.")
            pass

# By Alysa Solomon
def random_recipe_helper(search_func: SearchEngine.RecipeSearchEngine, user: User | None):
    req_ing = get_ingredients("In Arabic Numerals, How many ingredients do you want to include in the recipe?\n")
    get_value = True
    while get_value:
        print("How many recipes do you want?\n")
        try:
            choose = int(input())
            get_value = False
        except ValueError:
            print("Please input a valid input")
    if req_ing == []:
        return search_func.get_random_recipes(choose)
    f = Filter.Filter()
    return search_func.get_random_recipe_with_filter(choose,user,f)

def filter_helper():
    pass


# SORTING by Alysa Solomon
# TODO: Add filters and ranking
def search_by_name(search_func: SearchEngine.RecipeSearchEngine):
    will_continue = True
    while will_continue:
        search_str = input("Please input Name of Recipe: ")
        recipe_list = search_func.search_recipes_by_name(search_str)
        # print("Additonal Features not supported")
        return recipe_list
    pass
def search_by_category(search_func: SearchEngine.RecipeSearchEngine):
    # req_ing = get_ingredients("How many ingredients do you want to include in the recipe?\n")
    # ew_ing = get_ingredients("How many ingredients do you want to exclude from the recipe?\n")
    category = get_category()
    # dietary_list = get_dietary()
    recipe_list = search_func.search_recipes_by_category(category)
    return recipe_list
def search_by_ing(search_func: SearchEngine.RecipeSearchEngine):
    req_ing = get_ingredients("How many ingredients do you want to include in the recipe?\n")
    recipe_list = search_func.search_recipes_by_ingredients(req_ing)
    return recipe_list

def get_saved_dietary_preferences(user: User) -> list[str]:
    # Tolu: saved diet preferences as a list
    if user is None or not user.dietary_preferences:
        return []

    preferences = user.dietary_preferences.split(",")
    clean_preferences = []

    for preference in preferences:
        preference = preference.strip().lower()

        if preference:
            clean_preferences.append(preference)

    return clean_preferences


def apply_saved_dietary_preferences(recipe_list: list[Recipe], user: User) -> list[Recipe]:
    # apply saved diet preferences to search results
    if recipe_list is None:
        return []

    saved_preferences = get_saved_dietary_preferences(user)

    if not saved_preferences:
        return recipe_list

    filtered_recipes = []

    for recipe in recipe_list:
        recipe_tags = recipe.tags or []
        clean_tags = []

        for tag in recipe_tags:
            clean_tags.append(tag.strip().lower())

        matches_preferences = True

        for preference in saved_preferences:
            if preference not in clean_tags:
                matches_preferences = False

        if matches_preferences:
            filtered_recipes.append(recipe)

    return filtered_recipes

# By Thanvii Ambala
def reset_password(email: str, new_password: str, service: ServiceContainer) -> bool:
    """
    Reset a user's password.
    Returns True if successful, otherwise False.
    """
    email = email.strip().lower()

    if new_password == "":
        raise ValueError("New password cannot be empty")
    user = service.get_user_by_email(email)
    if user is None:
        print("User not found.")
        return False
    
    if service.change_password(user, new_password):
        print(f"Password for {email} was reset successfully.")
        return True

    return False

# By Thanvii Ambala
def reset_password_helper(service: ServiceContainer):
    email = input("Enter your email: ")
    new_password = input("Enter your new password: ")
    if email == "":
        print("Email cannot be empty.")
        raise ValueError("Email cannot be empty.")
    reset_password(email, new_password, service)

# By Thanvii Ambala
def change_password_helper(service: ServiceContainer, user: User):
    old_password = input("Enter your current password: ")
    if not service.authenticate_user(user.email, old_password):
        print("Current password is incorrect.")
        return
    new_password = input("Enter your new password: ")
    new_password_again = input("Re-enter your new password: ")
    if new_password == "":
        print("New password cannot be empty.")
        raise ValueError("New password cannot be empty.")
    if new_password != new_password_again:
        print("Passwords do not match.")
        return
    if service.change_password(user, new_password):
        print("Password changed successfully.")
    else:
        print("Error changing password.")

def update_account_info_helper(service: ServiceContainer, user: User):
    # Tolu: let user choose what account info to update
    is_updating = True

    while is_updating:
        print("\nUpdate Account Information")
        print("1: Update Email")
        print("2: Update Password")
        print("3: Update Dietary Preferences")
        print("4: Back")

        try:
            choice = int(input("Select your choice: "))

            match choice:
                case 1:
                    new_email = input("Enter your new email: ")

                    if service.update_email(user, new_email):
                        user.email = new_email.strip().lower()
                        print("Email updated successfully.")
                    else:
                        print("Email was not updated.")

                case 2:
                    change_password_helper(service, user)

                case 3:
                    new_preferences = input("Enter your dietary preferences: ")

                    if service.update_dietary_preferences(user, new_preferences):
                        user.dietary_preferences = new_preferences.strip()
                        print("Dietary preferences updated successfully.")
                    else:
                        print("Dietary preferences were not updated.")

                case 4:
                    is_updating = False

                case _:
                    print("Invalid option. Please try again.")

        except ValueError:
            print("Please input a valid input.")

#RANK by Alysa Solomon
def rank(recipe_list: List[Recipe]):
    r = Rank.Rank()
    get_choice = True
    while get_choice:
        try:
            print("Current Options are listed below")
            print("1: Rank by Newest")
            print("2: Rank by Popularity")
            option = int(input("Select your choice: "))
            match option:
                case 1:
                    recipes = r.rank_by_newest(recipe_list)
                    return recipes
                case 2:
                    recipes = r.rank_by_popularity(recipe_list)
                    return recipes
                case _:
                    print("Invalid Option. Please Try Again.")
                    pass
        except ValueError:
            print("Please input a valid input.")
            pass

# By Alysa Solomon
def search_not_logged_in(search_func: SearchEngine.RecipeSearchEngine, service: ServiceContainer):
    is_searching = True
    while is_searching:
        print("\nCurrent Options are listed below:")
        print("1: Search by Name")  # Somewhat Implemented
        print("2: Search by Specified Criteria") # Not Implemented
        print("3: Search by Necessary Ingredients") # Not Implemented
        print("4: Help")
        print("5: Back")
        try:
            chosen_option = input("Select your choice:")
            chosen_option = int(chosen_option)
            match chosen_option:
                case 1: # search by name
                    recipe_list = search_by_name(search_func)
                    if recipe_list is not None and recipe_list != []:
                            recipe_list = rank(recipe_list)
                            view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")
                case 2: # Search by Criteria
                    recipe_list = search_by_category(search_func)
                    if recipe_list != []:
                            recipe_list = rank(recipe_list)
                            view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")
                    pass
                case 3: # Search by Neccessary Ing
                    recipe_list = search_by_ing(search_func)
                    if recipe_list != []:
                            recipe_list = rank(recipe_list)
                            view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")
                    pass
                case 4: #Help Menu
                    print("1: You input a name of a recipe, and our database finds all recipes that have that name in it's title")
                    print("2: You give us a list of criteria and we will give you recipes that follow your requirements.")
                    print("3: You give us a recipe of ingredients you desire and we will find recipes that have those ingredients")
                    print("4: Descriptions of every menu option")
                    print("5: Stop Searching and go to previous menu")
                case 5: # Exit
                    is_searching = False
                    pass
                case _:
                    print("Invalid Option. Please Try Again.")
        except ValueError:
            print("Please input a valid input.")
            pass
        input("Press Enter to Continue")


def search_logged_in(search_func: SearchEngine.RecipeSearchEngine, user: User, service: ServiceContainer):
    # Tolu: search menu for logged-in users with saved diet preferences
    is_searching = True

    while is_searching:
        print("\nCurrent Options are listed below:")
        print("1: Search by Name")
        print("2: Search by Specified Criteria")
        print("3: Search by Necessary Ingredients")
        print("4: Help")
        print("5: Back")

        try:
            chosen_option = input("Select your choice:")
            chosen_option = int(chosen_option)

            match chosen_option:
                case 1:
                    recipe_list = search_by_name(search_func)
                    recipe_list = apply_saved_dietary_preferences(recipe_list, user)

                    if recipe_list is not None and recipe_list != []:
                        recipe_list = rank(recipe_list)
                        view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")

                case 2:
                    recipe_list = search_by_category(search_func)
                    recipe_list = apply_saved_dietary_preferences(recipe_list, user)

                    if recipe_list != []:
                        recipe_list = rank(recipe_list)
                        view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")

                case 3:
                    recipe_list = search_by_ing(search_func)
                    recipe_list = apply_saved_dietary_preferences(recipe_list, user)

                    if recipe_list != []:
                        recipe_list = rank(recipe_list)
                        view_recipe_results(recipe_list, service)
                    else:
                        print("No Recipes Found")

                case 4:
                    print("1: You input a name of a recipe, and our database finds recipes with that name.")
                    print("2: You give us criteria and we find recipes that follow your requirements.")
                    print("3: You give us ingredients and we find recipes that use those ingredients.")
                    print("4: Descriptions of every menu option")
                    print("5: Stop searching and go to previous menu")

                case 5:
                    is_searching = False

                case _:
                    print("Invalid Option. Please Try Again.")

        except ValueError:
            print("Please input a valid input.")

        input("Press Enter to Continue")

# By Alysa Solomon
def register_user(service: ServiceContainer):
    will_continue = True
    while will_continue:
        email = input("Please input your email: ")
        password = input("Please input a new password: ")
        password_check = input("Please type password again: ")
        if password_check == password:
            try:
                user = service.create_user(email,password)
                will_continue = False
                print("Account Succesfully Created.")
                return user
            except ValueError:
                print("Either your Password or your Email was not valid.\nPlease try again.")
                option = input("Continue? Type 'N' or 'No' to stop.\n")
                match option.lower():
                    case "n":
                        return None
                    case "no":
                        return None
                    case _:
                        pass
        else:
            option = input("Continue? Type 'N' or 'No' to stop.\n")
            match option.lower():
                case "n":
                    return None
                case "no":
                    return None
                case _:
                    pass

#By: Alysa Solomon and Jon Bailey
def get_pop_searches(service: ServiceContainer, search_engine: SearchEngine.RecipeSearchEngine) -> list[Recipe]:
    get_amount = True
    while get_amount:
        print("How many popular searches do you want? The default is 10. Press enter for default selection\n")

        try:
            raw = input()

            if raw == "":
                count = 10
            else:
                count = int(raw)

            popular = service.get_popular_searches(count)

            if not popular:
                print("No popular searches available.")
                return []

            print("\nPopular Searches:")
            for i, item in enumerate(popular, start=1):
                print(f"{i}. {item['query']} ({item['count']} searches)")

            choice = int(input("Select a search (number): "))

            if choice < 1 or choice > len(popular):
                print("Invalid choice.")
                continue  # 👈 don't exit, let them retry

        except ValueError:
            print("Please input a valid input")
            continue

        selected_query = popular[choice - 1]["query"]

        print(f"\nSearching for: {selected_query}")

        results = search_engine.search_recipes_by_name(selected_query)

        if results is None:
            return []
        return results
    # Fallback for type checker only.
    return []
    
# By Jon Bailey
def add_recipe(service: ServiceContainer):
    now = datetime.now()
    name = input("What do you want to call your recipe?").strip()
    if not name:
        print("Recipe name cannot be empty")
        return
    try:
        ing_num = int(input("How many ingredients does your recipe have?"))
        if ing_num < 0:
            raise ValueError
    except ValueError:
        print("Invalid number of ingredients")
        return
    
    ingredients = []
    for i in range (ing_num):
        ing = input(f"What is ingredient {i+1} called?").strip()
        if ing:
            ingredients.append(ing)
        else:
            print("Empty ingredient skipped")

    print("\nEnter instructions (type 'done' when finished):")
    instructions = []
    step = 1
    while True:
        line = input(f"Step {step}: ").strip()
        if line.lower() == "done":
            break
        if line:
            instructions.append(line)
            step += 1

    try:
        recipe = service.add_recipe(name = name, instructions = instructions, ingredients = ingredients, pub_time=now)
        if recipe is None:
            print("Error creating recipe, Recipe returned as None")
            raise
        print(f"\nRecipe: '{recipe.name}' added successfully.")
    except Exception as e:
        print(f"Error adding Recipe: {e}")

def delete_account(service: ServiceContainer, user: User):
    return service.delete_user(user)

#By Alysa Solomon
def main():
    service = ServiceContainer()
    search_func = SearchEngine.RecipeSearchEngine(service)
    user = None
    will_continue = True
    while(will_continue):
        if user != None:
            print("\nCurrent options are listed below. \nInput the number on the left to select your choice.")
            print("1: Get Popular Searches") #Not Implemented
            print("2: Get Random Recipe")  #Not Implemented
            print("3: Search for Recipe") #Not Implemented
            print("4: Add Your Own Recipe") #Not Implemented
            print("5: Add Ingredients to Pantry") #Not Implemented
            print("6: Update User Information")
            print("7: Log Out")
            print("8: Delete Account") #Not Implemented
            print("9: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                match chosen_option:
                    case 1: # Get Popular Searches
                        recipe_list = get_pop_searches(service,search_func)
                        recipe_list = apply_saved_dietary_preferences(recipe_list, user)
                        if recipe_list != []:
                            view_recipe_results(recipe_list, service)
                        else:
                            print("No Recipes Found.")
                        # print("BROKEN: WILL NOT WORK")
                        # print("UNCOMMENT OUT WHEN TESTING")
                    case 2: # Get Random Recipe
                        # TODO: NOT OUTPUTTING LIST OF RECIPES
                        recipe_list = random_recipe_helper(search_func, user)
                        if recipe_list != []:
                            view_recipe_results(recipe_list, service)
                        else:
                            print("No Recipes Found.")
                            pass
                    case 3: # Search for Recipe
                        search_logged_in(search_func, user, service)
                    case 4: # Add Recipe
                        #print("This feature hasn't been implemented yet.")
                        #pass
                        add_recipe(service)
                    case 5: # Add Ingredients to Pantry
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 6: # Update User Info
                        update_account_info_helper(service, user)
                    case 7: # Log Out
                        _, message, user = logout()
                        print(message)
                    case 8: # Delete Account
                        # print("This feature hasn't been implemented yet.")
                        # pass
                        if delete_account(user=user, service=service):
                            print("Account Successfully deleted.")
                            logged_in = False
                            user = None
                        else:
                            print("Account not deleted")
                    case 9: # Exit
                        will_continue = False
                        print("You will be automatically logged out.\nThank you for using our Program!")
                        pass
                    case _:
                        print("Invalid Option. Please Try Again.")
                        pass
                if chosen_option != 3:
                    input("Press Enter to Continue")
            except ValueError:
                print("Please input a valid input.")
                pass
            input("Press Enter to Continue")
        else:
            print("\nCurrent options are listed below. \nInput the number on the left to select your choice.")
            print("1: Log In")
            print("2: Get Popular Searches") # Not Working (Not Main.Py Issue)
            print("3: Get Random Recipe") # Not Working (Not Main.Py Issue)
            print("4: Create New Account") # Not Working (Not Main.Py Issue)
            print("5: Search for Recipe") # Somewhat Implemented
            print("6: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                match chosen_option:
                    case 1: # Log In  
                        user = loginHelper(service)
                        if user:
                            logged_in = True
                        if not logged_in:
                            print("Reseting Password has not been implemented yet.")
                            pass
                        input("Press Enter to Continue")
                    case 2: # Get Pop Searches
                        recipe_list = get_pop_searches(service,search_func)
                        if recipe_list != []:
                            view_recipe_results(recipe_list, service)
                        else:
                            print("No Recipes Found.")
                        # print("BROKEN: WILL NOT WORK")
                        # print("UNCOMMENT OUT WHEN TESTING")
                    case 3: # Get Random Recipe
                        # TODO: NOT OUTPUTTING LIST OF RECIPES
                        recipe_list = random_recipe_helper(search_func, user)
                        if recipe_list != []:
                            view_recipe_results(recipe_list, service)
                        else:
                            print("No Recipes Found.")
                            pass
                    case 4: # Register Account
                        user = register_user(service)
                    case 5: # Searching For a recipe
                        search_not_logged_in(search_func, service)
                    case 6: # Exit
                        will_continue = False
                        print("Thank you for using our Program!")
                    case _:
                        print("Invalid Option. Please Try Again.")
                if chosen_option != 5:
                    input("Press Enter to Continue")
            except ValueError:
                print("Please input a valid input.")
                pass
            
            pass
        pass
    service.close()



if __name__ == "__main__":
    main()

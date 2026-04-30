import os
from dotenv import load_dotenv
import pathlib
from db.database_operations import ServiceContainer
from model import Recipe, User
from model.auth import login, logout
from SearchEngine import SearchEngine
from typing import List

load_dotenv()

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

def loginHelper():
    # login part
    username = input("Enter username: ")
    password = input("Enter password: ")

    success, message = login(username, password)
    print(message)

    if success:
        print("You are now logged in!")
        return True
    
    return False

def logoutHelper():
    print(logout())
    return False

def retrieve_recipe(recipes: List[Recipe]):
    getting_recipe = True

def get_ingredients():
    count = 0
    gettingCount = True
    while gettingCount:
        try:
            count = input()
            count = int(count)
            gettingCount = False
        except ValueError:
            print("Please input a valid input.")
            pass

    ing_list = []
    print("Please input name of ingredients, one at a time.")
    for _ in range(count):
        ing_list.append(input())
    return ing_list

def get_category():
    category_list = ["Beef",
                     "Breakfast",
                     "Chicken","Dessert", 
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


def get_dietary():
    #TODO: I don't know if this is correct
    category_list = ["Algerian","American","Argentinian","Australian","British","Canadian","Chinese","Croatian","Dutch","Egyptian","Filipino","French","Greek","Indian","Irish","Italian","Jamaican","Japanese","Kenyan","Malaysian","Mexican","Moroccan","Norwegian","Polish","Portuguese","Russian","Saudi Arabian","Slovakian","Spanish","Syrian","Thai","Tunisian","Turkish","Ukrainian","Uruguayan","Venezulan","Vietnamese"]
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

def random_recipe_helper():
    print("In Arabic Numerals, How many ingredients do you want to include in the recipe?\n")
    req_ing = get_ingredients()
    get_value = True
    while get_value:
        print("In Arabic Numerals, How many recipes do you want?\n")
        try:
            choose = int(input())
            get_value = False
        except ValueError:
            print("Please input a valid input")
    search_func = SearchEngine.RecipeSearchEngine()
    if req_ing == []:
        return search_func.get_random_recipes(choose)
    f = filter()
    return search_func.get_random_recipe_with_filter(choose,req_ing,f)

def search_not_logged_in():
    is_searching = True
    search_func = SearchEngine.RecipeSearchEngine()
    while is_searching:
        print("Current Options are listed below:")
        print("1: Search by Name")  # Not Implemented
        print("2: Search by Specified Criteria") # Not Implemented
        print("3: Search by Necessary Ingredients") # Not Implemented
        print("4: Help")
        print("5: Back")
        try:
            chosen_option = input("Select your choice:")
            chosen_option = int(chosen_option)
            match chosen_option:
                case 1: # search by name
                    search_str = input("Please input Name of Recipe: ")
                    recipe_list = search_func.search_recipes_by_name(search_str)
                    print("Additonal Features not supported")
                    pass
                case 2: # Search by Criteria
                    print("This Feature has not been implemeted yet.")
                    print("In Arabic Numerals, How many ingredients do you want to include in the recipe?\n")
                    req_ing = get_ingredients()
                    print("In Arabic Numerals, How many ingredients do you want to exclude from the recipe?\n")
                    ew_ing = get_ingredients()
                    category = get_category()
                    dietary_list = get_dietary()
                    recipe_list = search_func.search_recipes_by_criteria(req_ing,ew_ing,category,dietary_list)
                    pass
                case 3: # Search by Neccessary Ing
                    print("This Feature has not been implemeted yet.")
                    print("In Arabic Numerals, How many ingredients do you want to include in the recipe?\n")
                    req_ing = get_ingredients()
                    recipe_list = search_func.search_recipes_by_ingredients(req_ing)
                    pass
                case 4: #Help Menu
                    print("1: You input a name of a recipe, and our database finds all recipes that have that name in it's title")
                    print("2: You give us a list of wanted ingredients, unwanted ingredients, any style of food, or dietary restrictions, and we will give you recipes that follow your requirements.")
                    print("3: You give us a recipe of ingredients you desire and we will find recipes that have those ingredients")
                    print("4: Descriptions of every menu option")
                    print("5: Stop Searching and go to previous menu")
                    input("Press enter to continue.")
                case 5: # Exit
                    is_searching = False
                    pass
                case _:
                    print("Invalid Option. Please Try Again.")
        except ValueError:
            print("Please input a valid input.")

#By Alysa Solomon
def main():
    service = ServiceContainer()
    logged_in = False
    will_continue = True
    while(will_continue):
        if logged_in:
            print("\nCurrent options are listed below. \nInput the number on the left to select your choice.")
            print("1: Get Popular Searches") #Not Implemented
            print("2: Get Random Recipe")  #Not Implemented
            print("3: Search for Recipe") #Not Implemented
            print("4: Add Your Own Recipe") #Not Implemented
            print("5: Add Ingredients to Pantry") #Not Implemented
            print("6: Update User Information") #Not Implemented
            print("7: Log Out")
            print("8: Delete Account") #Not Implemented
            print("9: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                match chosen_option:
                    case 1: # Get Popular Searches
                        print("This feature hasn't been implemented yet.")
                    case 2: # Get Random Recipe
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 3: # Search for Recipe
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 4: # Add Recipe
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 5: # Add Ingrediets to Pantry
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 6: # Update User Info
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 7: # Log Out
                        # TODO: Fix When Login Helper returns User ID
                        logoutHelper()
                        logged_in = False
                        pass
                    case 8: # Delete Account
                        print("This feature hasn't been implemented yet.")
                        pass
                    case 9: # Exit
                        will_continue = False
                        print("You will be automatically logged out.\nThank you for using our Program!")
                        pass
                    case _:
                        print("Invalid Option. Please Try Again.")
            except ValueError:
                print("Please input a valid input.")
        else:
            print("\nCurrent options are listed below. \nInput the number on the left to select your choice.")
            print("1: Log In")
            print("2: Get Popular Searches") # Not Implemented
            print("3: Get Random Recipe") # Not Tested
            print("4: Create New Account") # Not Implemented
            print("5: Search for Recipe") # Somewhat Implemented
            print("6: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                match chosen_option:
                    case 1: # Log In  
                        #TODO: fix when loginHelper returns a user ID
                        logged_in = loginHelper()
                        if not logged_in:
                            print("Reseting Password has not been implemented yet.")
                    case 2: # Get Pop Searches
                        print("This feature hasn't been implemented yet.")
                    case 3: # Get Random Recipe
                        # TODO: NOT OUTPUTTING LIST OF RECIPES
                        recipe_list = random_recipe_helper()
                        print(recipe_list)
                    case 4: # Register Account
                        print("This feature hasn't been implemented yet.")
                    case 5: # Searching For a recipe
                        search_not_logged_in()
                    case 6: # Exit
                        will_continue = False
                        print("Thank you for using our Program!")
                    case _:
                        print("Invalid Option. Please Try Again.")
                    
            except ValueError:
                print("Please input a valid input.")
                pass
            pass
        pass
    service.close()



if __name__ == "__main__":
    main()

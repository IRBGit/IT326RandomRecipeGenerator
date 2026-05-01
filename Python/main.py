import os
from dotenv import load_dotenv
import pathlib
from db.database_operations import ServiceContainer
from model import Recipe, User
from SearchEngine import SearchEngine, Filter, Rank
from typing import List

load_dotenv()

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
            count = input(outputString)
            count = int(count)
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
def random_recipe_helper():
    req_ing = get_ingredients("How many ingredients do you want to include in the recipe?\n")
    get_value = True
    while get_value:
        print("How many recipes do you want?\n")
        try:
            choose = int(input())
            get_value = False
        except ValueError:
            print("Please input a valid input")
    search_func = SearchEngine.RecipeSearchEngine()
    if req_ing == []:
        return search_func.get_random_recipes(choose)
    f = Filter.Filter()
    return search_func.get_random_recipe_with_filter(choose,req_ing,f)

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
def search_not_logged_in():
    is_searching = True
    search_func = SearchEngine.RecipeSearchEngine()
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
                    if recipe_list != []:
                            recipe_list = rank(recipe_list)
                            print(recipe_list)
                    else:
                        print("No Recipes Found")
                case 2: # Search by Criteria
                    recipe_list = search_by_category(search_func)
                    if recipe_list != []:
                            recipe_list = rank(recipe_list)
                            print(recipe_list)
                    else:
                        print("No Recipes Found")
                    pass
                case 3: # Search by Neccessary Ing
                    recipe_list = search_by_ing(search_func)
                    if recipe_list != []:
                            recipe_list = rank(recipe_list)
                            print(recipe_list)
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
def get_pop_searches(service: ServiceContainer, search_engine: SearchEngine.RecipeSearchEngine):
    while True:
        print("How many popular searches do you want? The default is 10. Press enter for default selection\n")

        try:
            raw = input()

            if raw.strip() == "":
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

        return results

#By Alysa Solomon
def main():
    service = ServiceContainer()
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
            print("6: Update User Information") #Not Implemented
            print("7: Log Out")
            print("8: Delete Account") #Not Implemented
            print("9: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                match chosen_option:
                    case 1: # Get Popular Searches
                        # recipe_list = get_pop_searches(service)
                        # if recipe_list != []:
                        #     print(recipe_list)
                        # else:
                        #     print("No Recipes Found.")
                        print("BROKEN: WILL NOT WORK")
                        print("UNCOMMENT OUT WHEN TESTING")
                    case 2: # Get Random Recipe
                        # TODO: NOT OUTPUTTING LIST OF RECIPES
                        recipe_list = random_recipe_helper()
                        if recipe_list != []:
                            print(recipe_list)
                        else:
                            print("No Recipes Found.")
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
                        _, message, user = logout()
                        print(message)
                    case 8: # Delete Account
                        print("This feature hasn't been implemented yet.")
                        pass
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
                        if user == None:
                            print("Reseting Password has not been implemented yet.")
                            pass
                        input("Press Enter to Continue")
                    case 2: # Get Pop Searches
                        # recipe_list = get_pop_searches(service)
                        # if recipe_list != []:
                        #     print(recipe_list)
                        # else:
                        #     print("No Recipes Found.")
                        print("BROKEN: WILL NOT WORK")
                        print("UNCOMMENT OUT WHEN TESTING")
                    case 3: # Get Random Recipe
                        # TODO: NOT OUTPUTTING LIST OF RECIPES
                        recipe_list = random_recipe_helper()
                        if recipe_list != []:
                            print(recipe_list)
                        else:
                            print("No Recipes Found.")
                            pass
                    case 4: # Register Account
                        user = register_user(service)
                    case 5: # Searching For a recipe
                        search_not_logged_in()
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

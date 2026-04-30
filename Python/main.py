import os
from dotenv import load_dotenv
import pathlib
from db.database_operations import ServiceContainer
from model import Recipe, User
from model.auth import login, logout

load_dotenv()

def add_note_to_recipe(
        service: ServiceContainer, 
        user: User, 
        recipe: Recipe
    ):
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

def delete_note_from_recipe(
        service: ServiceContainer,
        user: User
):
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

def main():
    logged_in = False
    will_continue = True
    while(will_continue):
        if logged_in:
            print("1: Get Popular Searches")
            print("2: Get Random Recipe")
            print("3: Search for Recipe")
            print("4: Add Your Own Recipe")
            print("5: Add Ingredients to Pantry")
            print("6: Update User Information")
            print("7: Search for Recipe")
            print("8: Log Out")
            print("9: Delete Account")
            print("10: Exit")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
            except ValueError:
                print("Please input a valid input.")
                continue
        else:
            print("1: Log In")
            print("2: Get Popular Searches")
            print("3: Get Random Recipe")
            print("4: Create New Account")
            print("5: Search for Recipe")
            print("6: Exit")
            logoutHelper()
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                if(1 <= chosen_option and chosen_option <= 6):
                    match chosen_option:
                        case 1: # Log In
                            is_logged_in = loginHelper()
                            if not is_logged_in:
                                print("Reseting Password has not been implemented yet.")
                        case 2: # Get Pop Searches
                            print("This feature hasn't been implemented yet.")
                        case 3: # Get Random Recipe
                            print("This feature hasn't been implemented yet.")
                        case 4: # Register Account
                            print("This feature hasn't been implemented yet.")
                        case 5: # Searching For a recipe
                            print("This feature hasn't been implemented yet.")
                        case 6: # Exit
                            will_continue = False
                            print("Thank you for using our Program!")
                    pass
                else:
                    print("Invalid Option. Please Try Again.")
            except ValueError:
                print("Please input a valid input.")

        # Delete once Exit is implemented in both sides.
        will_continue = False


if __name__ == "__main__":
    main()

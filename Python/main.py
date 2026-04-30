import os
from dotenv import load_dotenv

from model.auth import login, logout

load_dotenv()

def loginHelper():
        # login part
    username = input("Enter username: ")
    password = input("Enter password: ")

    success, message = login(username, password)
    print(message)
    return True

def logoutHelper():
    print(logout())
    return False

def main():
    logged_in = False
    will_continue = True
    while(will_continue):
        if logged_in:
            print("List all possible options in a list here")
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
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
                if(1 <= chosen_option and chosen_option <= 6):
                    # switch statement to to pick relevent helper method.
                    pass
                else:
                    print("Invalid Option. Please Try Again.")
            except ValueError:
                print("Please input a valid input.")
                continue
        will_continue = False

if __name__ == "__main__":
    main()
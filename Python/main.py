import os
from dotenv import load_dotenv
import pathlib

load_dotenv()

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
            print("List all possible options in a list here")
            try:
                chosen_option = input("Select your choice:")
                chosen_option = int(chosen_option)
            except ValueError:
                print("Please input a valid input.")
                continue
        will_continue = False

if __name__ == "__main__":
    main()
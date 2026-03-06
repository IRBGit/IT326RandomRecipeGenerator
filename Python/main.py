import os
from dotenv import load_dotenv
load_dotenv()

def main():
    stuff = os.getenv("WHATEVER")
    print(stuff)

if __name__ == "__main__":
    main()

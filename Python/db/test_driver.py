# driver.py
# This file tests if the database is connected to the file.

from db_connect import DBConnect

def main():
    # Create DBConnect instance
    db_connect = DBConnect()

    print("Attempting to connect to database...")

    try:
        #print("1")
        # Initialize engine
        db_connect.connect()
        #print("2")

        # Check connection
        if db_connect.is_connected():
            print("Database connection successful!")
        else:
            print("Database connection failed.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close session if one exists
        db_connect.close_session()
        print("Database session closed.")

if __name__ == "__main__":
    main()
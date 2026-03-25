# driver.py
# This file tests if the database is connected to the file.

from db.db_connect import DBConnect

def main():
    # Create DBConnect instance
    db_connect = DBConnect()

    print("Attempting to connect to database...")

    try:
        # Check connection
        if db_connect.test_connection():
            print("Database connection successful!")
        else:
            print("Database connection failed.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close session if one exists
        db_connect.shutdown()
        print("Database session closed.")

if __name__ == "__main__":
    try:
        main()
    finally:
        DBConnect().shutdown()
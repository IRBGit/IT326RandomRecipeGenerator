# seed_test.py
import sys
import os

# 1. Add current directory to path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database_operations import ServiceContainer

def run_seed():
    print("--- Initializing Service Container ---")
    # This triggers your DBConnect and all 4 services
    container = ServiceContainer()
    
    print("--- Seeding 10 Users ---")
    for i in range(1, 11):
        email = f"chef_{i}@example.com"
        # Using a password that satisfies your 3-of-4 character types rule
        password = f"SafePass{i}!" 
        
        try:
            user = container.create_user(email, password)
            if user:
                print(f" [SUCCESS] Created User {i}: {email}")
        except ValueError as e:
            # This catches 'User already exists' or 'Password not strong enough'
            print(f" [SKIPPED] {email}: {e}")

    print("\n--- Testing Retrieval ---")
    test_user = container.get_user_by_email("chef_1@example.com")
    if test_user:
        print(f" Verified: Found {test_user.email} in database.")

if __name__ == "__main__":
    try:
        run_seed()
    finally:
        ServiceContainer().close()
"""
    Authors: Thanvi Ambala 
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from model.user import User

def register_account(session: Session, email: str, password: str) -> User:
    """
    This function creates a new user account.

    Steps:
    1. Clean the email
    2. Check if user already exists
    3. Create new user
    4. Save to database
    """

    email = email.strip().lower()

    if email == "":
        raise ValueError("Email cannot be empty")

    if password == "":
        raise ValueError("Password cannot be empty")

    existing_user = session.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise ValueError("User already exists with this email")

    new_user = User(email=email, password=password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def delete_account(session: Session, email: str) -> bool:
    """
    Delete a user account using the user's email.

    Args:
        session: database session
        email: email of the account to delete

    Returns:
        True if deleted, False if user not found
    """
    email = email.strip().lower()

    user = session.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        print("User not found.")
        return False

    session.delete(user)
    session.commit()

    print(f"Account for {email} deleted.")
    return True

def reset_password(session: Session, email: str, new_password: str) -> bool:
    """
    Reset a user's password.
    Returns True if successful, otherwise False.
    """
    email = email.strip().lower()

    if new_password == "":
        raise ValueError("New password cannot be empty")

    user = session.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        print("User not found.")
        return False

    user.reset_password(new_password)
    session.commit()

    print(f"Password for {email} was reset successfully.")
    return True
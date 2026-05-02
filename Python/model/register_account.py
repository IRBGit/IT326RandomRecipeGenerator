"""
    Authors: Thanvi Ambala 
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from model.user import User

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
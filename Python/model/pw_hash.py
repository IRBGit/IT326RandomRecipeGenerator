"""
    Author: Jon Bailey and Thanvi Ambala
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class PWHash:
    """
    A class that will hash and verify passwords.

    Methods:
        hashPassword(password)
        verify(hash, password)
    """
    def __init__(self):
        self.ph = PasswordHasher()
    
    def hashPassword(self, password) -> str:
        """
        Hash a password to store in the database.
        """
        return self.ph.hash(password)
    
    def verify(self, hashed_password: str, password: str) -> bool:
        """
        A method that returns true or false based on it matching the stored hash from the database.

        Args:
            password(str): The password to verify against the hash
            hash(str): The hash string to be used to check the password.

        Returns:
            verified(bool): Returns True if the password matches the hash. Returns False if the password does not match the hash.
        """
        try:
            return self.ph.verify(hashed_password, password)

        except VerifyMismatchError:
            return False
        
    

            


"""
    Author: Jon Bailey
"""

from argon2 import PasswordHasher

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
        A method to hash a password into a hashstring to be stored in the database.

        Args:
            password(str): A password that you want to turn into a hash string.
        """
        hash = self.ph.hash(password)
        return hash
    
    def verify(self, hash, password) -> bool:
        """
        A method that returns true or false based on it matching the stored hash from the database.

        Args:
            password(str): The password to verify against the hash
            hash(str): The hash string to be used to check the password.

        Returns:
            verified(bool): Returns True if the password matches the hash. Returns False if the password does not match the hash.
        """
        try:
            self.ph.verify(hash, password)
            return True
        except:
            return False
    

            


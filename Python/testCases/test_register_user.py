"""
Author - Jon Bailey
"""

import unittest
from db.database_operations import ServiceContainer

class TestRegisterUser(unittest.TestCase):
    def setUp(self):
        self.service = ServiceContainer()
        self.created_users = []

    def tearDown(self):
        for user in self.created_users:
            self.service.delete_user(user)

    def test_register_user_success(self):
        email = "test@example.com"
        password = "StrongPass!"

        user = self.service.create_user(email, password)
        self.created_users.append(user)

        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)
        self.assertIsNotNone(user.id)
    
    def test_register_user_weak_password(self):
        email = "weak@example.com"
        password = "weak"

        with self.assertRaises(ValueError) as context:
            self.service.create_user(email, password)
        
        self.assertIn("not strong enough", str(context.exception))

    def test_register_user_duplicate_email(self):
        email = "duplicate@example.com"
        password = "StrongPass1!"

        user = self.service.create_user(email, password)
        self.created_users.append(user)

        with self.assertRaises(ValueError) as context:
            self.service.create_user(email, password)

        self.assertIn("already exists", str(context.exception))

    def test_register_user_password_is_hashed(self):
        email = "hash@example.com"
        password = "StrongPass1!"

        user = self.service.create_user(email, password)
        self.created_users.append(user)

        #Ensure password is not stored as plain text
        self.assertNotEqual(user.password, password)

        #Ensure authentication works
        authenticated = self.service.authenticate_user(email, password)
        self.assertIsNotNone(authenticated)
from model.user import User
from model.ingredient import Ingredient
from model.pantry import PantryItem
from model.recipe import Recipe
from model.associations import recipe_ingredients, user_favorites

from db.db_connect import DBConnect

db = DBConnect()
db.create_tables()
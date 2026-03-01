from model.user import User
from model.ingredient import Ingredient
from model.pantry import PantryItem
from model.recipe import Recipe
from model.associations import recipe_ingredients, user_favorites

from db.db_connect import DBConnect

# THIS WILL ONLY CREATE NEW TABLES!!! IT WILL NOT UPDATE EXISTING TABLES!
# TO REPLACE A TABLE USE THE DLL COMMAND IN SQL DEVELOPER:
## DROP TABLE ******* CASCADE CONSTRAINTS; ##

db = DBConnect()
db.create_tables()
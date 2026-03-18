from model import User, Ingredient, PantryItem, Recipe, recipe_ingredients, user_favorites
from db.db_connect import DBConnect

# THIS WILL ONLY CREATE NEW TABLES!!! IT WILL NOT UPDATE EXISTING TABLES!
# TO REPLACE A TABLE USE THE DDL COMMAND IN SQL DEVELOPER:
## DROP TABLE ******* CASCADE CONSTRAINTS; ##

db = DBConnect()
db.drop_tables()
db.create_tables()
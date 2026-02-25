

class ObjectCreator:
    """Static class for creating ORM objects."""

    @staticmethod
    def create_recipe(name: str, instructions: str = None):
        from model.recipe import Recipe
        return Recipe(name = name, instructions = instructions)
    
    @staticmethod
    def create_ingredient(name:str):
        from model.ingredient import Ingredient
        return Ingredient(name = name)
    
    

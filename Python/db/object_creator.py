# This class is built to create objects for methods
class ObjectCreator:
    # Static class for creating ORM objects.

    @staticmethod
    def create_recipe(recipe_model):
        """
        Create a recipe object from the database.

        Args:
            recipe_model(model): The output of the query.

        Return:
            Recipe: A new recipe object.
        """
        return recipe_model
    
    @staticmethod
    def create_ingredient(ingredient_model):
        """
        Create an ingredient object from the database.

        Args:
            ingredient_model(model): The output of the query.

        Return:
            Ingredient: A new Ingredient object.
        """
        return ingredient_model
    
    @staticmethod
    def create_user(user_model):
        """
        Create a User object from the database.
        
        Args:
            user_model(model): The output of the query.
            
        Return:
            User: A new User object.
        """
        from model.user import User
        return user_model
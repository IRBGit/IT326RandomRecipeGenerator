from sqlalchemy.orm import Session
from model import User, Recipe, Ingredient

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)

    def delete(self, obj):
        self.session.delete(obj)


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter_by(email=email).first()


class RecipeRepository(BaseRepository):
    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return self.session.get(Recipe, recipe_id)
    
    def get_by_name(self, recipe_name: str) -> Recipe | None:
        return self.session.query(Recipe).filter_by(name=recipe_name).first()
    
    def get_all(self) -> list[Recipe]:
        return self.session.query(Recipe).all()

class IngredientRepository(BaseRepository):
    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        return self.session.get(Ingredient, ingredient_id)
    
    def get_by_name(self, name: str) -> Ingredient | None:
        return self.session.query(Ingredient).filter_by(name=name).first()
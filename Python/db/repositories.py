from sqlalchemy.orm import Session
from model import User, Recipe, Ingredient, UserSearch

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
    
    def get_by_name(self, recipe_name: str) -> list[Recipe] | None:
        return list(self.session.query(Recipe).filter_by(name=recipe_name))
<<<<<<< HEAD
        
=======
    
>>>>>>> 971dc9f9eca41e22a2bfc117aa3902628c5d3757
    def get_all(self) -> list[Recipe]:
        return self.session.query(Recipe).all()

class IngredientRepository(BaseRepository):
    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        return self.session.get(Ingredient, ingredient_id)
    
    def get_by_name(self, name: str) -> Ingredient | None:
        return self.session.query(Ingredient).filter_by(name=name).first()
    
class SearchRepository(BaseRepository):
    def get_by_id(self, search_id: int):
        return self.session.get(UserSearch, search_id)
    
    def get_recent(self, limit: int = 50):
        return(
            self.session.query(UserSearch)
            .order_by(UserSearch.timestamp.desc())
            .limit(limit)
            .all()
        )
    
    def get_popular(self, limit: int = 10):
        from sqlalchemy import func

        return(
            self.session.query(
                UserSearch.query,
                func.count(UserSearch.query).label("count")
            )
            .group_by(UserSearch.query)
            .order_by(func.count(UserSearch.query).desc())
            .limit(limit)
            .all()
        )
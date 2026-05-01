from sqlalchemy.orm import Session
from model import User, Recipe, Ingredient, UserSearch
from sqlalchemy import func

class BaseRepository:
    # By Jon Bailey
    def __init__(self, session: Session):
        self.session = session

    # By Jon Bailey
    def add(self, obj):
        self.session.add(obj)

    # By Jon Bailey
    def delete(self, obj):
        self.session.delete(obj)


class UserRepository(BaseRepository):
    # By Jon Bailey
    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    # By Jon Bailey
    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter_by(email=email).first()


class RecipeRepository(BaseRepository):
    # By Jon Bailey
    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return self.session.get(Recipe, recipe_id)
    
    # By Jon Bailey
    def search_by_name(self, recipe_name: str) -> list[Recipe]:
        return list(self.session.query(Recipe).filter(Recipe.name.ilike(f"%{recipe_name}%")))
    
    def get_by_name(self, recipe_name: str) -> Recipe | None:
        return self.session.query(Recipe).filter(Recipe.name == recipe_name).first()
    
    # By Jon Bailey
    def get_all(self) -> list[Recipe]:
        return self.session.query(Recipe).all()

class IngredientRepository(BaseRepository):
    # By Jon Bailey
    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        return self.session.get(Ingredient, ingredient_id)
    
    # By Jon Bailey
    def get_by_name(self, name: str) -> Ingredient | None:
        return self.session.query(Ingredient).filter_by(name=name).first()
    
class SearchRepository(BaseRepository):
    # By Jon Bailey
    def get_by_id(self, search_id: int):
        return self.session.get(UserSearch, search_id)
    
    # By Jon Bailey
    def get_recent(self, limit: int = 50):
        return(
            self.session.query(UserSearch)
            .order_by(UserSearch.timestamp.desc())
            .limit(limit)
            .all()
        )
    
    # By Jon Bailey
    def get_popular(self, limit: int = 10):
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
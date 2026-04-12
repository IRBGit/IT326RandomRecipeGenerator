from sqlalchemy.orm import Session
from db.db_connect import DBConnect
from db.repositories import UserRepository, RecipeRepository, IngredientRepository, SearchRepository

class UnitOfWork:
    def __init__(self):
        self.db = DBConnect()
        self.session: Session | None = None

    def __enter__(self):
        self.session = self.db.get_session()

        # Repositories get THIS session
        self.users = UserRepository(self.session)
        self.recipes = RecipeRepository(self.session)
        self.ingredients = IngredientRepository(self.session)
        self.searches = SearchRepository(self.session)

        return self

    def __exit__(self, exc_type, exc, tb):
        assert self.session is not None
        if exc:
            self.session.rollback()
        else:
            self.session.close()

    def commit(self):
        assert self.session is not None
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def rollback(self):
        assert self.session is not None
        self.session.rollback()
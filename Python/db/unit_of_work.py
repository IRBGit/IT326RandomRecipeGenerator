from sqlalchemy.orm import Session
from db.db_connect import DBConnect
from db.repositories import UserRepository, RecipeRepository, IngredientRepository, SearchRepository

class UnitOfWork:
    # By Jon Bailey
    def __init__(self):
        self.session: Session | None = None
        self.db = DBConnect()

    # By Jon Bailey
    def __enter__(self):

        self.session = self.db.get_session()

        # Repositories get THIS session
        self.users = UserRepository(self.session)
        self.recipes = RecipeRepository(self.session)
        self.ingredients = IngredientRepository(self.session)
        self.searches = SearchRepository(self.session)

        return self

    # By Jon Bailey
    def __exit__(self, exc_type, exc, tb):
        assert self.session is not None
        if exc:
            self.session.rollback()

        self.session.close()

    # By Jon Bailey
    def commit(self):
        assert self.session is not None
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    # By Jon Bailey
    def rollback(self):
        assert self.session is not None
        self.session.rollback()
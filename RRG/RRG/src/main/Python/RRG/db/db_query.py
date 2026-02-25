# db_query.py
from sqlalchemy.exc import SQLAlchemyError

class DBQuery:
    """Handles queries and transactions using SQLAlchemy."""

    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.session = self.db_connect.get_session()

    # -------------------- CRUD / Query Methods -------------------- #
    def add(self, obj):
        try:
            self.session.add(obj)
        except SQLAlchemyError as e:
            print(f"Add failed: {e}")
            raise

    def delete(self, obj):
        try:
            self.session.delete(obj)
        except SQLAlchemyError as e:
            print(f"Delete failed: {e}")
            raise

    def query(self, model):
        """Start a query for the given ORM model."""
        return self.session.query(model)

    # -------------------- Transaction Methods -------------------- #
    def begin_transaction(self):
        self.session.begin()

    def commit_transaction(self):
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(f"Commit failed: {e}")
            self.session.rollback()
            raise

    def rollback_transaction(self):
        self.session.rollback()

    # -------------------- Utility -------------------- #
    def close(self):
        self.session.close()
        self.session = None
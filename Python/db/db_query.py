# db_query.py
from sqlalchemy.exc import SQLAlchemyError

class DBQuery:
    """ Handles queries and transactions using SQLAlchemy and oracledb"""
    # Handles queries and transactions using SQLAlchemy.

    def __init__(self, db_connect):
        """
        The constructor for this class.

        Args:
            db_connect(DBConnect) = A DBConnect object.
        
        """
        self.db_connect = db_connect
        self.session = self.db_connect.get_session()

    # -------------------- CRUD / Query Methods -------------------- #
    def add(self, obj):
        """
        Add an item to the database.

        Args:
            obj(model): The model object that is being loaded (User, Recipe, etc.)
        """
        try:
            self.session.add(obj)
        except SQLAlchemyError as e:
            print(f"Add failed: {e}")
            raise

    def delete(self, obj):
        """
        Delete an item from the databse.

        Args:
            obj(model): The model object that is being deleted (User, Recipe, etc.)
        """
        try:
            self.session.delete(obj)
        except SQLAlchemyError as e:
            print(f"Delete failed: {e}")
            raise

    def query(self, model):
        """
        Start a query for the given ORM model.
        
        Args:
            model: The model object / table that you are querying (User, Recipe, etc...)
        """
        return self.session.query(model)

    # -------------------- Transaction Methods -------------------- #
    def begin_transaction(self):
        """
        Initiate this before doing any database actions.
        """
        self.session.begin()

    def commit_transaction(self):
        """
        Initiate this to commit data to the databse.
        """
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(f"Commit failed: {e}")
            self.session.rollback()
            raise

    def rollback_transaction(self):
        """
        Initiate this to undo the last commit to the database.
        """
        self.session.rollback()

    # -------------------- Utility -------------------- #
    def close(self):
        """
        Close the database connection.
        """
        self.session.close()
        self.session = None
# db_query.py
"""
    Author: Jon Bailey
"""

from sqlalchemy.exc import SQLAlchemyError
from db.db_connect import DBConnect
from sqlalchemy.orm import Query, Session


class DBQuery:
    """ Handles queries and transactions using SQLAlchemy and oracledb"""
    _instance = None

    def __new__(cls, db_connect):
        if cls._instance is None:
            cls._instance = super(DBQuery, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_connect: DBConnect):
        """
        The constructor for this class.

        Args:
            db_connect(DBConnect) = A DBConnect object.
        
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self.db_connect = db_connect
        self.session = self.db_connect.get_session()

        self._initialized = True

        print("DBQuery initialized (singleton)")
    
    def _get_session(self) -> Session:
        if self.session is None:
            self.session = self.db_connect.get_session()
        return self.session

    # -------------------- CRUD / Query Methods -------------------- #
    def add(self, obj):
        """
        Add an item to the database.

        Args:
            obj(model): The model object that is being loaded (User, Recipe, etc.)
        """
        
        session = self._get_session()

        try:
            session.add(obj)
        except SQLAlchemyError as e:
            print(f"Add failed: {e}")
            raise

    def delete(self, obj):
        """
        Delete an item from the databse.

        Args:
            obj(model): The model object that is being deleted (User, Recipe, etc.)
        """
        session = self._get_session()

        try:
            session.delete(obj)
        except SQLAlchemyError as e:
            print(f"Delete failed: {e}")
            raise

    def query(self, model) -> Query:
        """
        Start a query for the given ORM model.
        
        Args:
            model: The model object / table that you are querying (User, Recipe, etc...)
        """
        session = self._get_session()

        return session.query(model)

    # -------------------- Transaction Methods -------------------- #
    def begin_transaction(self):
        """
        Initiate this before doing any database actions.
        """
        session = self._get_session()

        if not session.in_transaction():
            session.begin()

    def commit_transaction(self):
        """
        Initiate this to commit data to the databse.
        """
        session = self._get_session()

        try:
            session.commit()
        except SQLAlchemyError as e:
            print(f"Commit failed: {e}")
            session.rollback()
            raise

    def rollback_transaction(self):
        """
        Initiate this to undo the last commit to the database.
        """
        session = self._get_session()

        session.rollback()

    # -------------------- Utility -------------------- #
    def close(self):
        """
        Close the database connection.
        """
        if self.session:
            self.session.close()
            self.session = None
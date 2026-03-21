# db_connect.py
"""
    Author: Jon Bailey
"""
from sqlalchemy.orm import Session

class DBConnect:
    """
    You must be connected via Cisco Secure Client VPN to the ISU network to access the database.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnect, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.exc import SQLAlchemyError
        from model import Base
        import os
        from dotenv import load_dotenv

        load_dotenv()

        db_pw = os.getenv("DB_PW")
        if not db_pw:
            raise ValueError("DB_PW not found")
        
        self.URL = f"oracle+oracledb://IT326S01:{db_pw}@10.110.10.90:1521/oracle"

        try:
            self.engine = create_engine(self.URL, echo = False, future = True)
            self.SessionLocal = sessionmaker(
                bind = self.engine, 
                autoflush = False, 
                autocommit = False
            )
            if self.SessionLocal:
                print("Connected successfully")
        except SQLAlchemyError as e:
            print(f"Database connection failed: {e}")
            self.engine = None
            raise

        self._initialized = True

    def get_session(self) -> Session:
        """
        Return a session.
        """
        return self.SessionLocal()

    def is_connected(self) -> bool:
        """
        Check if you have a connection to the databse.

        Returns:
            connected(bool): True if connected, False is not.
        """
        from sqlalchemy.exc import SQLAlchemyError
        if self.engine is None:
            print("self.engine is None")
            return False
        try:
            with self.engine.connect():
                print("Engine connection opened")
            return True
        except SQLAlchemyError as e:
            print (f"Connection failed with error: {e}")
            return False
    
    def create_tables(self):
        from model import Base
        if self.engine is None:
            raise RuntimeError("Engine not initialized")
        
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        from model import Base
        from sqlalchemy.exc import SQLAlchemyError
        if self.engine is None:
            raise RuntimeError("Engine not initialize")
        
        try:
            print("Attempting to drop all tables...")
            Base.metadata.drop_all(self.engine)
            print("All tables dropped successfully.")
        except SQLAlchemyError as e:
            print(f"Failed to drop tables: {e}")
            raise

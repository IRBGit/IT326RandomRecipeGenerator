# db_connect.py
"""
    Author: Jon Bailey
"""
from sqlalchemy.orm import Session

class DBConnect:
    """
    You must be connected via Cisco Secure Client VPN to the ISU network to access the database.

    If you are on ISUs network wifi, you need to ensure you are not using a private VPN.
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

    def test_connection(self) -> bool:
        from sqlalchemy import text
        if self.engine is None:
            return False
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1 FROM DUAL"))
            return True
        except Exception as e:
            print (f"COnnection test failed: {e}")
            return False
        
    def shutdown(self):
        """
        Clean up database resources (Close connection pool).

        CALL ONLY WHEN EXITING THE PROGRAM.
        """
        if self.engine:
            print("Freeing database engine")
            self.engine.dispose()
    
    def create_tables(self):
        from model import Base
        if self.engine is None:
            raise RuntimeError("Engine not initialized")
        
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        from model import Base
        from sqlalchemy.exc import SQLAlchemyError
        if self.engine is None:
            raise RuntimeError("Engine not initialized")
        
        try:
            print("Attempting to drop all tables...")
            Base.metadata.drop_all(self.engine)
            print("All tables dropped successfully.")
        except SQLAlchemyError as e:
            print(f"Failed to drop tables: {e}")
            raise

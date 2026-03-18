# db_connect.py
"""
    Author: Jon Bailey
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from model.base import Base
import os
from dotenv import load_dotenv
load_dotenv()

class DBConnect:
    """
    You must be connected via Cisco Secure Client VPN to the ISU network to access the database.
    """
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.session = None
        db_pw = os.getenv("DB_PW")
        if not db_pw:
            raise ValueError("DB_PW not found in environment variables")
        self.URL = f"oracle+oracledb://IT326S01:{db_pw}@10.110.10.90:1521/oracle"

    def connect(self):
        if self.engine is None:
            try:
                self.engine = create_engine(self.URL, echo=False, future=True)
                self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
                print("Connected successfully")
            except SQLAlchemyError as e:
                print(f"Database connection failed: {e}")
                self.engine = None
                raise

    def get_session(self) -> Session:
        """
        Return a session.
        """
        if self.SessionLocal is None:
            self.connect()

        if self.SessionLocal is None:
            raise RuntimeError("Failed to create SessionLocal. Check your database connection.")
        
        if self.session is None:
            self.session = self.SessionLocal()
        return self.session

    def close_session(self):
        """
        Close the session.
        """
        if self.session is not None:
            self.session.close()
            self.session = None

    def is_connected(self) -> bool:
        """
        Check if you have a connection to the databse.

        Returns:
            connected(bool): True if connected, False is not.
        """
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
    
    def get_engine(self):
        if self.engine is None:
            self.connect()
        return self.engine
    
    def create_tables(self):
        engine = self.get_engine()
        Base.metadata.create_all(engine)

    def drop_tables(self):
        engine = self.get_engine()
        try:
            print("Attempting to drop all tables...")
            Base.metadata.drop_all(engine)
            print("All tables dropped successfully.")
        except SQLAlchemyError as e:
            print(f"Failed to drop tables: {e}")
            raise

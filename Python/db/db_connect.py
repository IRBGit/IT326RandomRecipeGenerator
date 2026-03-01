# db_connect.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from model.base import Base

class DBConnect:
    # You must be connected to the VPN via Cisco SecureClient to be
    # able to connect to the database
    URL = "oracle+oracledb://IT326S01:store55@10.110.10.90:1521/oracle"

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.session = None

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
        if self.SessionLocal is None:
            self.connect()
        if self.session is None:
            self.session = self.SessionLocal()
        return self.session

    def close_session(self):
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
            return False
        try:
            with self.engine.connect():
                print("Engine connection opened")
            return True
        except SQLAlchemyError as e:
            print (f"COnnection failed iwth error: {e}")
            return False
    
    def get_engine(self):
        if self.engine is None:
            self.connect()
        return self.engine
    
    def create_tables(self):
        engine = self.get_engine()
        Base.metadata.create_all(engine)
# db_connect.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

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
        if self.engine is None:
            return False
        try:
            with self.engine.connect():
                print("Engine connection opened")
            return True
        except SQLAlchemyError as e:
            print (f"COnnection failed iwth error: {e}")
            return False
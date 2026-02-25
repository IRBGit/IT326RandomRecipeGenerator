# db_connect.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

class DBConnect:
    URL = "oracle+oracledb://IT326:store55@10.110.10.90:1521/?sid=oracle"

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.session = None

    def connect(self):
        if self.engine is None:
            try:
                self.engine = create_engine(self.URL, echo=False, future=True)
                self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
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
            with self.engine.connect() as conn:
                conn.execute("SELECT 1 FROM DUAL")
            return True
        except SQLAlchemyError:
            return False
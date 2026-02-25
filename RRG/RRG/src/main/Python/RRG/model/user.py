# models.py (continuing from Recipe)
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from model.recipe import Recipe

# Assuming Base is already defined earlier
Base = declarative_base()

# Association table for many-to-many relationship between User and Recipe
user_favorites = Table(
    'user_favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Many-to-many relationship to Recipe
    favorites = relationship(
        "Recipe",
        secondary=user_favorites,
        backref="favorited_by"
    )

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def check_password(self, password: str) -> bool:
        return self.password == password

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
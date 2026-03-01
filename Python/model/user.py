# models.py (continuing from Recipe)
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base
from model.associations import user_favorites

# Association table for many-to-many relationship between User and Recipe


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

    pantry_items = relationship(
        "PantryItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def check_password(self, password: str) -> bool:
        return self.password == password

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
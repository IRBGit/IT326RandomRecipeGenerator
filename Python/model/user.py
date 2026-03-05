# models.py (continuing from Recipe)
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from model.base import Base
from model.associations import user_favorites
from model.pw_hash import PWHash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, 
                Sequence('user_id_seq'),
                primary_key=True)
    email = Column(String(255), 
                   unique=True, 
                   nullable=False)
    password = Column(String(255), 
                      nullable=False)

    # Many-to-many relationship to Recipe
    favorites = relationship(
        "Recipe",
        secondary=user_favorites,
        back_populates="favorited_by"
    )

    pantry_items = relationship(
        "PantryItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = PWHash().hashPassword(password)

    def check_password(self, toCheck: str) -> bool:
        return PWHash().verify(hash = self.password, password = toCheck)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
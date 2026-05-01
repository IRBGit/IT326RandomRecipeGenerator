# associations.py
"""
    Author: Jon Bailey
"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from model.base import Base

# By Jon Bailey
user_favorites = Table(
    'user_favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True)
)
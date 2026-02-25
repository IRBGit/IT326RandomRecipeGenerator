from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Table, Column, ForeignKey

Base = declarative_base()

recipe_ingredients = Table(
    "recipe_ingredients", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
    
)

class Recipe(Base):
    __tablename__ = "recipes" # Table name in the SQL database

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable = False)
    area = Column()
    instructions = Column(Text, nullable=True)
    

    # This relationship is automatically created via the backref in User and explicitly identified here.
    favorited_by = relationship("User", secondary = "user_favorites", back_populates = "favorites")

    def __init__(self, name: str, instructions: str = None):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"<Recipe(id = {self.id}, name ='{self.name}')>"
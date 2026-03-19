from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from model.base import Base

class Rating(Base):
    __tablename__ = "ratings"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key = True)

    rating = Column(Integer, nullable = False)

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name = "check_rating_range"),
    )

    #Relationships
    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")

    def __repr__(self):
        return f"Rating(user_id = {self.user_id}, recipe_id = {self.recipe_id}, rating = {self.rating})>"

"""
Author: Jon Bailey
"""

from __future__ import annotations
from sqlalchemy import Sequence, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base import Base

class UserSearch(Base):
    __tablename__ = "user_searches"

    id: Mapped[int] = mapped_column(
        Integer, 
        Sequence("search_id_seq"),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable = True
    )

    query: Mapped[str] = mapped_column(
        String(255), 
        nullable = False
    )

    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False
    )

    user = relationship("User", back_populates = "searches")
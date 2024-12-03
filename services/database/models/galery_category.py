from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Int64, TimestampMixin

if TYPE_CHECKING:
    from services.database.models import Galery


class GaleryCategory(Base, TimestampMixin):
    __tablename__ = "galery_category"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100), unique=True)
    images: Mapped[List[Galery]] = relationship('Galery', back_populates='category', cascade='all, delete-orphan')

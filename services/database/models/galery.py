from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, Int64, TimestampMixin

if TYPE_CHECKING:
    from .galery_category import GaleryCategory


class Galery(Base, TimestampMixin):
    __tablename__ = "img_galery"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    img_id: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('galery_category.id'))
    category: Mapped[GaleryCategory] = relationship('GaleryCategory', back_populates='images')

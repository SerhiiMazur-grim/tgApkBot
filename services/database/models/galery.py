from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class Galery(Base, TimestampMixin):
    __tablename__ = "img_galery"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    img_id: Mapped[str]

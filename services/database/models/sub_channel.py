from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class SubChannel(Base, TimestampMixin):
    __tablename__ = "sub_channel"
    
    id: Mapped[Int64] = mapped_column(primary_key=True)
    username: Mapped[str]

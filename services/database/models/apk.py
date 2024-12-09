from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class APK1(Base, TimestampMixin):
    __tablename__ = "apk1"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String())
    file_id: Mapped[str] = mapped_column(String())
    caption_en: Mapped[str] = mapped_column(String())
    caption_ua: Mapped[str] = mapped_column(String())
    caption_ru: Mapped[str] = mapped_column(String())


class APK2(Base, TimestampMixin):
    __tablename__ = "apk2"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String())
    file_id: Mapped[str] = mapped_column(String())
    caption_en: Mapped[str] = mapped_column(String())
    caption_ua: Mapped[str] = mapped_column(String())
    caption_ru: Mapped[str] = mapped_column(String())

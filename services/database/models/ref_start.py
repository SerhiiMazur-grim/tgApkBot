from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class RefMessage(Base, TimestampMixin):
    __tablename__ = "ref_start_text"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ref: Mapped[str] = mapped_column(String(length=64))
    ref_url: Mapped[str] = mapped_column(String())
    en: Mapped[str] = mapped_column(String())
    ua: Mapped[str] = mapped_column(String())
    ru: Mapped[str] = mapped_column(String())

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class SubChannel(Base, TimestampMixin):
    __tablename__ = "sub_channel"
    
    id: Mapped[Int64] = mapped_column(primary_key=True)
    username: Mapped[str]
    invate_url: Mapped[str]

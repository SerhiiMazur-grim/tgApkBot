from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .user import UserRepository
from .sub_channel import SubChannelRepository
from .galery import GaleryRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    user: UserRepository
    sub_channel: SubChannelRepository
    galery: GaleryRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.user = UserRepository(session=session)
        self.sub_channel = SubChannelRepository(session=session)
        self.galery = GaleryRepository(session=session)

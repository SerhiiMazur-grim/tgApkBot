from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .user import UserRepository
from .sub_channel import SubChannelRepository
from .galery import GaleryRepository
from .ref_start import RefMessageRepository
from .apk import APK1Repository, APK2Repository
from .galery_category import CategoryRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    user: UserRepository
    sub_channel: SubChannelRepository
    galery: GaleryRepository
    ref_message: RefMessageRepository
    apk1: APK1Repository
    apk2: APK2Repository
    category: CategoryRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.user = UserRepository(session=session)
        self.sub_channel = SubChannelRepository(session=session)
        self.galery = GaleryRepository(session=session)
        self.ref_message = RefMessageRepository(session=session)
        self.apk1 = APK1Repository(session=session)
        self.apk2 = APK2Repository(session=session)
        self.category = CategoryRepository(session=session)

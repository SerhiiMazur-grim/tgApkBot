from typing import Optional, cast, List

from aiogram import Bot
from sqlalchemy import select, update, values, delete

from ..models import APK1, APK2
from .base import BaseRepository


class APK1Repository(BaseRepository):
    async def get_by_id(self, id: str | int) -> Optional[APK1]:
        id = int(id)
        return cast(
            Optional[APK1],
            await self._session.scalar(select(APK1).where(APK1.id == id)),
        )
    
    
    async def get(self):
        rez = await self._session.scalars(select(APK1))
        return rez.all()[-1]
    
    
    async def create_apk(self, name: str, file_id: str, caption_en: str, caption_ua: str, caption_ru: str):
        apk: APK1 = APK1(name=name,
                         file_id=file_id,
                         caption_en=caption_en,
                         caption_ua=caption_ua,
                         caption_ru=caption_ru)
        await self.commit(apk)
    
    
    async def update_apk(self, id: str|int, name: str, file_id: str, caption_en: str, caption_ua: str, caption_ru: str):
        apk: APK1 = await self.get_by_id(id)
        apk.name = name
        apk.file_id = file_id
        apk.caption_en=caption_en
        apk.caption_ua=caption_ua
        apk.caption_ru=caption_ru
        await self.commit(apk)
    
    
    async def delete_apk(self, id):
        id = int(id)
        rez = await self._session.execute(
            delete(APK1).where(APK1.id == id).returning(APK1)
        )
        deleted_apk = rez.scalars().first()
        await self.commit()
        return deleted_apk


class APK2Repository(BaseRepository):
    async def get_by_id(self, id: str | int) -> Optional[APK2]:
        id = int(id)
        return cast(
            Optional[APK2],
            await self._session.scalar(select(APK2).where(APK2.id == id)),
        )
    
    
    async def get(self):
        rez = await self._session.scalars(select(APK2))
        return rez.all()[-1]
    
    
    async def create_apk(self, name: str, file_id: str, caption_en: str, caption_ua: str, caption_ru: str):
        apk: APK2 = APK2(name=name,
                         file_id=file_id,
                         caption_en=caption_en,
                         caption_ua=caption_ua,
                         caption_ru=caption_ru)
        await self.commit(apk)
    
    
    async def update_apk(self, id: str|int, name: str, file_id: str, caption_en: str, caption_ua: str, caption_ru: str):
        apk: APK2 = await self.get_by_id(id)
        apk.name = name
        apk.file_id = file_id
        apk.caption_en=caption_en
        apk.caption_ua=caption_ua
        apk.caption_ru=caption_ru
        await self.commit(apk)
    
    
    async def delete_apk(self, id):
        id = int(id)
        rez = await self._session.execute(
            delete(APK2).where(APK2.id == id).returning(APK2)
        )
        deleted_apk = rez.scalars().first()
        await self.commit()
        return deleted_apk

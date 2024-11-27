from typing import Optional, cast, List

from aiogram import Bot
from sqlalchemy import select, update, values, delete

from ..models import RefMessage
from .base import BaseRepository


class RefMessageRepository(BaseRepository):
    async def get(self, ref: str) -> Optional[RefMessage]:
        return cast(
            Optional[RefMessage],
            await self._session.scalar(select(RefMessage).where(RefMessage.ref == ref)),
        )
    
    
    async def get_all_ref(self) -> list[RefMessage]:
        result = await self._session.scalars(select(RefMessage))
        return result.all()
    
    
    async def get_ref_message(self, ref: str, local: str):
        if local == 'ru':
            return await self._session.scalar(select(RefMessage.ru).where(RefMessage.ref == ref))
        elif local == 'uk':
            return await self._session.scalar(select(RefMessage.ua).where(RefMessage.ref == ref))
        else:
            return await self._session.scalar(select(RefMessage.en).where(RefMessage.ref == ref))            
    
    
    async def create_ref(self, bot: Bot, ref: str, en: str, uk: str, ru: str):
        me = await bot.get_me()
        bot_username = me.username
        new_ref_messages: RefMessage = RefMessage(
            ref = ref,
            ref_url = f't.me/{bot_username}?start={ref}',
            en = en,
            ua = uk,
            ru = ru
        )
        await self.commit(new_ref_messages)
        return new_ref_messages
    
    
    async def delete_ref(self, ref_id):
        ref_id = int(ref_id)
        rez = await self._session.execute(
            delete(RefMessage).where(RefMessage.id == ref_id).returning(RefMessage)
        )
        deleted_ref = rez.scalars().first()
        await self.commit()
        return deleted_ref.ref

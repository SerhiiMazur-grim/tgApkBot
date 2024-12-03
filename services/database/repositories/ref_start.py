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
        db_ref: RefMessage = await self.get(ref)
        img = db_ref.img
        if local == 'ru':
            msg = db_ref.ru
            btn = db_ref.btn_ru
            answer = db_ref.answer_ru
        elif local == 'uk':
            msg = db_ref.ua
            btn = db_ref.btn_ua
            answer = db_ref.answer_ua
        else:
            msg = db_ref.en
            btn = db_ref.btn_en
            answer = db_ref.answer_en
        return img, msg, btn, answer
    
    
    async def create_ref(self, bot: Bot, data: dict[str]):
        me = await bot.get_me()
        bot_username = me.username
        ref = data['ref']
        new_ref_messages: RefMessage = RefMessage(
            ref = ref,
            ref_url = f't.me/{bot_username}?start={ref}',
            img = data['img'],
            en = data['en'],
            ua = data['ua'],
            ru = data['ru'],
            btn_en = data['btn_en'],
            btn_ua = data['btn_ua'],
            btn_ru = data['btn_ru'],
            answer_en = data['answer_en'],
            answer_ua = data['answer_ua'],
            answer_ru = data['answer_ru']
        )
        await self.commit(new_ref_messages)
        return new_ref_messages.ref_url
    
    
    async def delete_ref(self, ref_id):
        ref_id = int(ref_id)
        rez = await self._session.execute(
            delete(RefMessage).where(RefMessage.id == ref_id).returning(RefMessage)
        )
        deleted_ref = rez.scalars().first()
        await self.commit()
        return deleted_ref.ref

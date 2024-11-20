from typing import Optional, cast, List

from aiogram import Bot
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import SubChannel
from .base import BaseRepository


class SubChannelRepository(BaseRepository):
    
    async def get(self, channel_id: int) -> Optional[SubChannel]:
        return cast(
            Optional[SubChannel],
            await self._session.scalar(select(SubChannel).where(SubChannel.id == channel_id)),
        )
    
    async def get_all_channels(self) -> list[SubChannel]:
        result = await self._session.scalars(select(SubChannel))
        return result.all()

    
    async def channels_ids(self) -> List[int]:
        rez = await self._session.scalars(select(SubChannel.id))
        return rez.all()
    
    async def channels_usernames(self) -> List[str]:
        rez = await self._session.scalars(select(SubChannel.username))
        return rez.all()
        

    async def create_from_telegram(self, bot: Bot, channel_username: str,
                                   invate_url: str) -> SubChannel:
        channel: Chat = await bot.get_chat(chat_id=channel_username)
        sub_channel: SubChannel = SubChannel(
            id = channel.id,
            username = '@' + channel.username,
            invate_url = invate_url
        )
        
        await self.commit(sub_channel)
        return sub_channel
    
    async def delete_channel(self, channel_id: str | int) -> None:
        channel_id = int(channel_id)
        rez = await self._session.execute(
            delete(SubChannel).where(SubChannel.id == channel_id).returning(SubChannel)
        )
        deleted_channel = rez.scalars().first()
        await self.commit()
        return deleted_channel.username
        

from typing import Optional, cast

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
    
    async def get_all_channels(self) -> Optional[SubChannel]:
        return cast(
            Optional[SubChannel],
            await self._session.scalars(select(SubChannel)),
        )

    async def create_from_telegram(self, bot: Bot, channel_username: str) -> SubChannel:
        channel: Chat = await bot.get_chat(chat_id=channel_username)
        sub_channel: SubChannel = SubChannel(
            id = channel.id,
            username = '@' + channel.username
        )
        
        await self.commit(sub_channel)
        return sub_channel
    
    async def delete_channel(self, channel_id: str) -> None:
        channel: SubChannel = await self._session.scalar(
            delete(SubChannel)
            .where(SubChannel.id == channel_id)
        )
        await self.commit(channel)

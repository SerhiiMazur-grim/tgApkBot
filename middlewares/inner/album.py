import asyncio
from typing import Any, Union, Optional, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: Union[int, float] = 0.2) -> None:
        self.latency = latency
        self.album_data = {}
    
    def callect_album_messages(self, event: Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {'messages': []}
        self.album_data[event.media_group_id]['messages'].append(event)
        
        return len(self.album_data[event.media_group_id]['messages'])
    
    
    async def __call__(
        self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message, data: dict[str, Any]) -> Optional[Any]:
        
        if not event.media_group_id:
            data['album'] = None
            return await handler(event, data)
        
        total_before = self.callect_album_messages(event)
        await asyncio.sleep(self.latency)
        total_after = len(self.album_data[event.media_group_id]['messages'])
        
        if total_before != total_after:
            return
        
        album_messages: list = self.album_data[event.media_group_id]['messages']
        album_messages.sort(key=lambda x: x.message_id)
        data['album'] = album_messages
        
        await handler(event, data)
        
        del self.album_data[event.media_group_id]

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, cast

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User, Message
from aiogram_i18n import I18nMiddleware

from config.users import USERS

if TYPE_CHECKING:
    from services.database import DBUser, Repository


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")
        referal = None
        
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)
        
        if event.message:
            if event.message.text:
                if event.message.text.startswith('/start'):
                    split_text = event.message.text.split()
                                
                    if (
                        len(split_text) > 1 
                        and split_text[0] == "/start"
                    ):
                        referal = split_text[1]
        
        user = USERS.get(aiogram_user.id)
        if not user:
            repository: Repository = data["repository"]
            user: Optional[DBUser] = await repository.user.get(user_id=aiogram_user.id)
            if user is None:
                i18n: I18nMiddleware = data["i18n_middleware"]
                user = await repository.user.create_from_telegram(
                    user=aiogram_user,
                    locale=(
                        aiogram_user.language_code
                        if aiogram_user.language_code in i18n.core.available_locales
                        else cast(str, i18n.core.default_locale)
                    ),
                    referal=referal,
                    chat=chat,
                )
            USERS[aiogram_user.id] = user

        data['user'] = user

        return await handler(event, data)

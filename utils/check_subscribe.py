import os
import logging
from typing import TYPE_CHECKING, List

from aiogram import Bot
from aiogram.types import Message
from aiogram_i18n import I18nContext

from config.settings import Settings
from app.keyboards.inline_kb.user_ikb import channel_list_to_sub_ikb

from services.database import Repository, DBUser


settings = Settings()


async def is_subscribe(message: Message, bot: Bot, i18n: I18nContext,
                        user: DBUser, repository: Repository):
    if user.id == settings.admin_chat_id:
        return True
    
    channels_list = await repository.sub_channel.get_all_channels()
    if not channels_list:
        return True

    not_sub_list = []
    for channel in list(channels_list):
        try:
            member = await bot.get_chat_member(chat_id=channel.id, user_id=user.id)
            if member.status not in ['member', 'creator', 'administrator']:
                    not_sub_list.append(channel)
        except Exception as e:
            await bot.send_message(chat_id=settings.admin_chat_id,
                                   text=f'Failed to check subscription for channel {channel.username}: {e}')

    if not_sub_list:
        await repository.user.update_user_subscribe(user=user, subscribe=False)
        await message.answer(text=i18n.messages.you_not_sub(),
                            reply_markup=channel_list_to_sub_ikb(i18n, not_sub_list))
        return False
    
    else:
        await repository.user.update_user_subscribe(user)
        return True

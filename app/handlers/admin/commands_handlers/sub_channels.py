from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import SubChannel
from app.state.admin_state import GetChannelUsernameState, DelSubChannelState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb, del_sub_channel_ikb

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(Command('add_sub_channel'))
async def add_sub_channel(message: Message, i18n: I18nContext,
                          state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(GetChannelUsernameState.username)
    
    return message.answer(text=i18n.messages.get_channel_username(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(GetChannelUsernameState.username)
async def get_sub_channel_username(message: Message, bot: Bot, i18n: I18nContext,
                                   state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    if not message.text:
        return message.answer(text=i18n.messages.is_not_channel_username(),
                              reply_markup=abort_command_ikb(i18n))
    username: str = message.text.strip()
    if not username.startswith('@'):
        username = '@' + username
    await state.update_data(username=username)
    await state.set_state(GetChannelUsernameState.invate_url)
    return message.answer(text=i18n.messages.get_invate_url(),
                          reply_markup=abort_command_ikb(i18n))
    

@router.message(GetChannelUsernameState.invate_url)
async def get_invate_url(message: Message, bot: Bot, i18n: I18nContext,
                        state: FSMContext, repository: Repository):
    if not message.text:
        return message.answer(text=i18n.messages.is_not_invate_url(),
                              reply_markup=abort_command_ikb(i18n))
    username = await state.get_value('username')
    await state.clear()
    try:
        await repository.sub_channel.create_from_telegram(bot, username, message.text.strip())
        return message.answer(text=i18n.messages.sub_channel_added())
    except:
        return message.answer(text=i18n.messages.something_went_wrong())


@router.message(Command('all_sub_channel'))
async def show_sub_channels(message: Message, i18n: I18nContext,
                            repository: Repository) -> TelegramMethod[Any]:
    await message.delete()
    usernames: List[str] = await repository.sub_channel.get_all_channels_usernames()
    if usernames:
        usernames.insert(0, '')
        channels_list: str = '\n➡️'.join(usernames)
    else:
        return message.answer(text=i18n.messages.no_sub_channels())
    
    return message.answer(text=i18n.messages.sub_channel_list(channels_list=channels_list))


@router.message(Command('delete_sub_channel'))
async def get_sub_channel_to_del(message: Message, i18n: I18nContext,
                          state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    await message.delete()
    channels: List[SubChannel] = await repository.sub_channel.get_all_channels()
    if list(channels):
        await state.set_state(DelSubChannelState.id)
        
        return message.answer(text=i18n.messages.delete_sub_channel(),
                            reply_markup=del_sub_channel_ikb(i18n, channels))
    else:
        return message.answer(text=i18n.messages.no_sub_channels())


@router.callback_query(DelSubChannelState.id)
async def del_sub_channel(callback_query: CallbackQuery, i18n: I18nContext,
                          state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    await callback_query.message.delete()
    await state.clear()
    channel_id: str = callback_query.data
    username = await repository.sub_channel.delete_channel(channel_id)
    
    return callback_query.message.answer(text=i18n.messages
                                         .sub_channel_is_delete(username=username))

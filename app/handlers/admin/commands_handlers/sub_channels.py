from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import SubChannel
from app.state.admin_state import GetChannelUsernameState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(Command('add_sub_channel'))
async def add_sub_channel(message: Message, i18n: I18nContext,
                          state: FSMContext):
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
        
    if message.text.startswith('@'):
        username: str = message.text.strip()
    elif message.text.startswith('t.me/'):
        username: str = '@' + message.text.split('/')[-1].strip()
    else:
        return message.answer(text=i18n.messages.is_not_channel_username(),
                              reply_markup=abort_command_ikb(i18n))
        
    await state.clear()
    try:
        await repository.sub_channel.create_from_telegram(bot, username)
        return message.answer(text=i18n.messages.sub_channel_added())
    except:
        return message.answer(text=i18n.messages.something_went_wrong())

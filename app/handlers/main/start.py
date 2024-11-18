from __future__ import annotations

from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import DBUser
from app.keyboards.reply_kb.user_rkb import main_keyboard
from app.filters import PrivateChatFilter
from utils import clear_state


router: Final[Router] = Router(name=__name__)


@router.message(PrivateChatFilter(), CommandStart())
async def start_command(message: Message, i18n: I18nContext, state: FSMContext, user: DBUser) -> TelegramMethod[Any]:
    await clear_state(state)
    
    return message.answer(text=i18n.messages.start(name=user.name),
                          reply_markup=main_keyboard(i18n))

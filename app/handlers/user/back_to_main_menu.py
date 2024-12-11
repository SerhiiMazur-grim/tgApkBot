from __future__ import annotations

from typing import Any, Final

from aiogram import Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from app.keyboards.reply_kb.user_rkb import main_keyboard
from app.filters import PrivateChatFilter
from utils import clear_state


router: Final[Router] = Router(name=__name__)


@router.message(PrivateChatFilter(), F.text == LazyProxy('button-back_to_main_rkb'))
async def back_to_main_menu_handler(message: Message, i18n: I18nContext, state: FSMContext) -> TelegramMethod:
    await clear_state(state)
    return message.answer(text=i18n.messages.main_menu(),
                          reply_markup=main_keyboard(i18n))
from __future__ import annotations

from typing import Any, Final

from aiogram import Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import DBUser, Repository
from app.keyboards.inline_kb.user_ikb import choose_lang_ikb
from app.keyboards.reply_kb.user_rkb import main_keyboard
from app.filters import PrivateChatFilter
from utils import clear_state
from config.users import USERS


router: Final[Router] = Router(name=__name__)


@router.message(PrivateChatFilter(), Command('language'))
async def init_change_lang(message: Message, state: FSMContext, i18n: I18nContext) -> TelegramMethod[Any]:
    await clear_state(state)
    return message.answer(text=i18n.messages.choose_language(),
                          reply_markup=choose_lang_ikb())


@router.callback_query(F.data.startswith('language'))
async def change_lang(callback_query: CallbackQuery, i18n: I18nContext,
                      user: DBUser, repository: Repository) -> TelegramMethod[Any]:
    await callback_query.message.delete()
    language: str = callback_query.data.split('_')[-1]
    await i18n.manager.set_locale(language, user, repository)
    user_id = callback_query.from_user.id
    user: DBUser = await repository.user.get(user_id)
    USERS[int(user_id)] = user
    
    return callback_query.message.answer(text=i18n.core.get('messages-language_is_set', language),
                                         reply_markup=main_keyboard(i18n, language))

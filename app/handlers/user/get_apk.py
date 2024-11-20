from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from app.filters import PrivateChatFilter
from config.callback_data import APK_1, APK_2
from utils import clear_state, is_subscribe

if TYPE_CHECKING:
    from services.database import DBUser, SubChannel, Repository


router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == APK_1)
async def get_apk_1_handler(callback_query: CallbackQuery, bot:Bot, user: DBUser,
                            i18n: I18nContext, state: FSMContext, repository: Repository) -> TelegramMethod:
    await clear_state(state)
    await callback_query.message.delete()
    
    return callback_query.message.answer(text='APK 1 load!')
    


@router.callback_query(F.data == APK_2)
async def get_apk_2_handler(callback_query: CallbackQuery, bot:Bot, user: DBUser,
                            i18n: I18nContext, state: FSMContext, repository: Repository) -> TelegramMethod:
    await clear_state(state)
    await callback_query.message.delete()
    
    return callback_query.message.answer(text='APK 2 load!')
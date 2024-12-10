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
    from services.database import DBUser, SubChannel, Repository, APK1, APK2


router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == APK_1)
async def get_apk_1_handler(callback_query: CallbackQuery,
                            i18n: I18nContext, user: DBUser, state: FSMContext, repository: Repository) -> TelegramMethod:
    await clear_state(state)
    await callback_query.message.delete()
    apk1 = await repository.apk1.get()
    local = user.locale
    if local == 'ru':
        caption = apk1.caption_ru
    elif local == 'uk':
        caption = apk1.caption_ua
    else:
        caption = apk1.caption_en
    
    return callback_query.message.answer_document(document=apk1.file_id, caption=caption)
    


@router.callback_query(F.data == APK_2)
async def get_apk_2_handler(callback_query: CallbackQuery,
                            i18n: I18nContext, user: DBUser, state: FSMContext, repository: Repository) -> TelegramMethod:
    await clear_state(state)
    await callback_query.message.delete()
    apk2 = await repository.apk2.get()
    local = user.locale
    if local == 'ru':
        caption = apk2.caption_ru
    elif local == 'uk':
        caption = apk2.caption_ua
    else:
        caption = apk2.caption_en
    
    return callback_query.message.answer_document(document=apk2.file_id, caption=caption)

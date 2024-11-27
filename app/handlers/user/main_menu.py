from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from app.keyboards.inline_kb.user_ikb import apk_files_ikb, galery_ikb
from app.filters import PrivateChatFilter
from app.state.user_state import CatalogState
from utils import clear_state, is_subscribe
from app.dialogs.user_dialogs import CatalogDialog

if TYPE_CHECKING:
    from services.database import DBUser, Repository


router: Final[Router] = Router(name=__name__)


@router.message(PrivateChatFilter(), F.text == LazyProxy('button-get_apk'))
async def get_apk_handler(message: Message, bot:Bot, user: DBUser,
                            i18n: I18nContext, state: FSMContext, repository: Repository) -> TelegramMethod:
    await clear_state(state)
    await message.delete()
    
    rez = await is_subscribe(message, bot, i18n, user, repository)
    if not rez:
        return
    
    return message.answer(text=i18n.messages.choose_apk(),
                          reply_markup=apk_files_ikb(i18n))


@router.message(PrivateChatFilter(), F.text == LazyProxy('button-galery'))
async def to_galery(message: Message, i18n: I18nContext, state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    user_id = message.chat.id
    await clear_state(state)
    await message.delete()
    
    catalog = await repository.galery.get_all_image_ids()
    if not catalog:
        return message.answer(text=i18n.messages.catalog_empty())
    
    await state.set_state(CatalogState.page)
    await state.update_data({
        'catalog': catalog,
        'pages': len(catalog),
        'page': 1,
    })
    return message.answer_photo(photo=catalog[0],
                                reply_markup=galery_ikb('1', len(catalog), user_id))


@router.callback_query(CatalogState.page)
async def galery_dialog(callback_query: CallbackQuery = None, state: FSMContext = None, repository: Repository = None):
    user_id = callback_query.from_user.id
    dialog = CatalogDialog(callback_query, state, repository, user_id)
    await dialog.dialog_window()

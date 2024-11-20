from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from app.keyboards.inline_kb.user_ikb import apk_files_ikb
from app.filters import PrivateChatFilter
from utils import clear_state, is_subscribe

if TYPE_CHECKING:
    from services.database import DBUser, SubChannel, Repository


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
async def to_galery(message: Message, i18n: I18nContext, state: FSMContext) -> TelegramMethod[Any]:
    await clear_state(state)
    await message.delete()
    
    return message.answer(text='Go to galery SUCSSES!!!')

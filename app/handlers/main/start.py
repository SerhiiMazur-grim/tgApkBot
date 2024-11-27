from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import DBUser
from app.keyboards.reply_kb.user_rkb import main_keyboard
from app.filters import PrivateChatFilter
from utils import clear_state

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(PrivateChatFilter(), CommandStart())
async def start_command(message: Message, i18n: I18nContext,
                        state: FSMContext, user: DBUser,
                        repository: Repository) -> TelegramMethod[Any]:
    await clear_state(state)
    text = i18n.messages.start(name=user.name)
    
    param = message.text.split()
    if len(param) > 1:
        text = await repository.ref_message.get_ref_message(ref=param[-1],
                                                            local=user.locale)
        text = f'👋{user.name}\n{text}'
    
    return message.answer(text=text,
                          reply_markup=main_keyboard(i18n))

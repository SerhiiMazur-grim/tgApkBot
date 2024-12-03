from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import SubChannel
from app.filters import PrivateChatFilter
from app.state.admin_state import AddCategoryState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb
from utils import clear_state

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(Command('add_category'))
async def start_add_category(message: Message, i18n: I18nContext,
                                  state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await clear_state(state)
    await state.set_state(AddCategoryState.cat)
    
    return message.answer(text=i18n.messages.send_category(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(AddCategoryState.cat)
async def get_category(message: Message, i18n: I18nContext, state: FSMContext, repository: Repository):
    title: str = message.text
    if not title:
        return message.answer(text=i18n.messages.is_not_cat())
    await state.clear()
    title_list = title.split('\n')
    if len(title_list)!=3:
        return message.answer(text=i18n.messages.is_not_cat())

    category = '\n'.join(title_list)
    await repository.category.create_category(title_list)
    return message.answer(text=i18n.messages.cat_is_created(category=category))

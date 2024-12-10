from __future__ import annotations

from typing import Any, Final

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import Repository, DBUser
from app.state.admin_state import GetImageIdState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb


router: Final[Router] = Router(name=__name__)


@router.message(Command('image_id'))
async def get_image_id_command(message: Message, i18n: I18nContext, user: DBUser,
                               state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(GetImageIdState.image)
    language: str = user.locale
    return message.answer(text=i18n.messages.send_image_to_get_id(),
                          reply_markup=abort_command_ikb(i18n, language))


@router.message(GetImageIdState.image)
async def get_image(message: Message, i18n: I18nContext, state: FSMContext) -> TelegramMethod[Any]:
    if message.photo:
        image_id = message.photo[-1].file_id
        await state.clear()
        return message.answer(text=image_id)
    else:
        return message.answer(text=i18n.messages.is_not_image_for_get_id())

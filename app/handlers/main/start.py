from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import DBUser, Repository
from app.keyboards.reply_kb.user_rkb import main_keyboard
from app.keyboards.inline_kb.user_ikb import ref_st_ikb
from app.filters import PrivateChatFilter
from app.state.user_state import UserRefStartState
from utils import clear_state, is_subscribe
from config.settings import Settings
# if TYPE_CHECKING:
#     from services.database import Repository


router: Final[Router] = Router(name=__name__)
s = Settings()

@router.message(PrivateChatFilter(), CommandStart())
async def start_command(message: Message, i18n: I18nContext,
                        state: FSMContext,
                        user: DBUser,
                        repository: Repository) -> TelegramMethod[Any]:

    await clear_state(state)
    
    param = message.text.split()
    if len(param) > 1:
        img, text, ikb_text, answer = await repository.ref_message.get_ref_message(ref=param[-1],
                                                            local=user.locale)
        text = f'👋{user.name}\n{text}'
        await state.set_state(UserRefStartState.ref)
        await state.update_data(answer=answer)
        return message.answer_photo(
            photo=img,
            caption=text,
            reply_markup=ref_st_ikb(ikb_text)
        )
    
    text = i18n.messages.start(name=user.name)
    return message.answer(text=text,
                          reply_markup=main_keyboard(i18n))


@router.callback_query(UserRefStartState.ref)
async def ref_start(call: CallbackQuery, bot: Bot, i18n: I18nContext, user: DBUser, state: FSMContext, repository: Repository):

    if not call.message.photo:
            await call.message.delete()
    is_sub = await is_subscribe(call, bot, i18n, user, repository)
    if is_sub:
        answer = await state.get_value('answer')
        await state.clear()
        return call.message.answer(text=answer,
                                   reply_markup=main_keyboard(i18n))

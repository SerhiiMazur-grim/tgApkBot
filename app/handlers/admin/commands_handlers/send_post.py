from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

# from services.database import APK1, APK2
from app.state.admin_state import PostState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb, send_post_ikb
from config.callback_data import SEND_POST
from utils import MessageMailer

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(Command('send_post_to_all'))
async def start_post(message: Message, i18n: I18nContext, state: FSMContext):
    await message.delete()
    await state.set_state(PostState.post)
    
    return message.answer(text=i18n.messages.send_me_post(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(PostState.post)
async def get_post(message: Message, i18n: I18nContext, state: FSMContext):
    await state.update_data(post=message)
    post: Message = await state.get_value('post')
    user_id = message.from_user.id
    await message.answer(text=i18n.messages.is_post())
    await post.copy_to(chat_id=user_id, reply_markup=post.reply_markup)
    await state.set_state(PostState.send)
    return message.answer(text=i18n.messages.send_this_post(),
                          reply_markup=send_post_ikb(i18n))


@router.callback_query(PostState.send)
async def send_post(call: CallbackQuery, i18n: I18nContext, state: FSMContext, repository: Repository):
    await call.message.delete()
    if not call.data == SEND_POST:
        await state.clear()
    msg: Message = await state.get_value('post')
    await state.clear()
    return await MessageMailer.start_mailing(msg, repository)

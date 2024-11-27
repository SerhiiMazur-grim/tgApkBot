from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import RefMessage
from app.state.admin_state import GetRefStartState, DelRefStartState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb, del_ref_ikb

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


async def wrong_data(message: Message, i18n: I18nContext):
    return message.answer(text=i18n.messages.ref_wrong_data(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(Command('add_ref_start'))
async def add_ref_start(message: Message, i18n: I18nContext,
                          state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(GetRefStartState.ref)
    
    return message.answer(text=i18n.messages.add_ref(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(GetRefStartState.ref)
async def get_ref(message: Message, i18n: I18nContext, 
                  state: FSMContext) -> TelegramMethod[Any]:
    if not message.text:
        return await wrong_data(message, i18n)
    elif len(message.text) > 64:
        return message.answer(text=i18n.messages.ref_too_long(),
                              reply_markup=abort_command_ikb(i18n))
    
    await state.update_data(ref=message.text)
    await state.set_state(GetRefStartState.en)
    return message.answer(text=i18n.messages.add_en_text())


@router.message(GetRefStartState.en)
async def get_ref_en(message: Message, i18n: I18nContext, 
                  state: FSMContext) -> TelegramMethod[Any]:
    if not message.text:
        return await wrong_data(message, i18n)
    
    await state.update_data(en=message.text)
    await state.set_state(GetRefStartState.ua)
    return message.answer(text=i18n.messages.add_ua_text())


@router.message(GetRefStartState.ua)
async def get_ref_ua(message: Message, i18n: I18nContext, 
                  state: FSMContext) -> TelegramMethod[Any]:
    if not message.text:
        return await wrong_data(message, i18n)
    
    await state.update_data(ua=message.text)
    await state.set_state(GetRefStartState.ru)
    return message.answer(text=i18n.messages.add_ru_text())


@router.message(GetRefStartState.ru)
async def get_ref_ru(message: Message, bot: Bot, i18n: I18nContext, 
                  state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    if not message.text:
        return await wrong_data(message, i18n)
    
    data: dict = await state.get_data()
    ref=data.get('ref')
    await state.clear()
    ref_start = await repository.ref_message.create_ref(
        bot=bot,
        ref=data.get('ref'),
        en=data.get('en'),
        ua=data.get('ua'),
        ru=message.text
    )
    return message.answer(text=i18n.messages.ref_created(ref=ref_start.ref_url))


@router.message(Command('delete_ref_start'))
async def get_ref_start_to_del(message: Message, i18n: I18nContext,
                          state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    await message.delete()
    ref_messages: List[RefMessage] = await repository.ref_message.get_all_ref()
    if list(ref_messages):
        await state.set_state(DelRefStartState.id)
        
        return message.answer(text=i18n.messages.choose_ref_to_dell(),
                            reply_markup=del_ref_ikb(i18n, ref_messages))
    else:
        return message.answer(text=i18n.messages.no_sub_channels())


@router.callback_query(DelRefStartState.id)
async def dell_ref_message(callback_query: CallbackQuery, i18n: I18nContext,
                          state: FSMContext, repository: Repository) -> TelegramMethod[Any]:
    await callback_query.message.delete()
    await state.clear()
    ref_message_id: str = callback_query.data
    ref: str = await repository.ref_message.delete_ref(ref_message_id)
    
    return callback_query.message.answer(text=i18n.messages.ref_is_dell(ref=ref))

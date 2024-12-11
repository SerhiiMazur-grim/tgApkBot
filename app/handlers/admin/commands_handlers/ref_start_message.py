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
    await state.set_state(GetRefStartState.img)
    return message.answer(text=i18n.messages.add_ref_img())


@router.message(GetRefStartState.img)
async def get_ref_img(message: Message, i18n: I18nContext, state: FSMContext):
    img = message.photo
    if not img:
        return message.answer(text=i18n.messages.is_not_image_for_get_id())
    await state.update_data(img=img[-1].file_id)
    await state.set_state(GetRefStartState.en)
    return message.answer(text=i18n.messages.add_ref_text())


@router.message(GetRefStartState.en)
async def get_ref_text(message: Message, i18n: I18nContext, state: FSMContext):
    txt_list: list[str] = message.text.split('+')
    if len(txt_list) != 3:
        return message.answer(text=i18n.messages.mis_text())
    await state.update_data(en=txt_list[0])
    await state.update_data(ua=txt_list[1])
    await state.update_data(ru=txt_list[2])
    await state.set_state(GetRefStartState.btn_en)
    return message.answer(text=i18n.messages.add_ref_btn_text())


@router.message(GetRefStartState.btn_en)
async def get_ref_btn_text(message: Message, i18n: I18nContext, state: FSMContext):
    btn_txt_list: list[str] = message.text.split('+')
    if len(btn_txt_list) != 3:
        return message.answer(text=i18n.messages.mis_text())
    await state.update_data(btn_en=btn_txt_list[0])
    await state.update_data(btn_ua=btn_txt_list[1])
    await state.update_data(btn_ru=btn_txt_list[2])
    await state.set_state(GetRefStartState.answer_en)
    return message.answer(text=i18n.messages.add_ref_answer_text())


@router.message(GetRefStartState.answer_en)
async def get_ref_answer_text(message: Message, bot: Bot, i18n: I18nContext,
                              state: FSMContext, repository: Repository):
    answer_list: list[str] = message.text.split('+')
    if len(answer_list) != 3:
        return message.answer(text=i18n.messages.mis_text())
    await state.update_data(answer_en=answer_list[0])
    await state.update_data(answer_ua=answer_list[1])
    await state.update_data(answer_ru=answer_list[2])
    data = await state.get_data()
    await state.clear()
    ref_url = await repository.ref_message.create_ref(bot, data)
    return message.answer(text=i18n.messages.ref_created(ref=ref_url))
    

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

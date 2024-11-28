from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import APK1, APK2
from app.state.admin_state import LoadApkState, UpdateApkState
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb, update_apk_ikb
from config.callback_data import APK1_CALL, APK2_CALL

if TYPE_CHECKING:
    from services.database import Repository


router: Final[Router] = Router(name=__name__)


@router.message(Command('upload_apk1'))
async def add_apk1(message: Message, i18n: I18nContext,
                          state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(LoadApkState.caption)
    await state.update_data(apk='apk1')
    
    return message.answer(text=i18n.messages.send_apk_caption(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(Command('upload_apk2'))
async def add_apk2(message: Message, i18n: I18nContext,
                          state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(LoadApkState.caption)
    await state.update_data(apk='apk2')
    
    return message.answer(text=i18n.messages.send_apk_caption(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(LoadApkState.caption)
async def get_apk_caption(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    caption = message.text
    await state.update_data(caption=caption)
    await state.set_state(LoadApkState.file)
    
    return message.answer(text=i18n.messages.upload_apk())


@router.message(LoadApkState.file)
async def get_apk_file(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    file = message.document
    if not file:
        return message.answer(text=i18n.messages.is_not_apk_file())
    apk = await state.get_value('apk')
    caption = await state.get_value('caption')
    await state.clear()
    if apk == 'apk1':
        await repository.apk1.create_apk(name=file.file_name,
                                         file_id=file.file_id,
                                         caption=caption)
    elif apk == 'apk2':
        await repository.apk2.create_apk(name=file.file_name,
                                         file_id=file.file_id,
                                         caption=caption)
        
    return message.answer(text=i18n.messages.upload_apk_ok(name=file.file_name))


@router.message(Command('update_apk'))
async def update_apk1(message: Message, i18n: I18nContext,
                          state: FSMContext, repository: Repository):
    await message.delete()
    await state.set_state(UpdateApkState.id)
    apk1 = await repository.apk1.get()
    apk2 = await repository.apk2.get()
    
    return message.answer(text=i18n.messages.choose_apk_to_update(),
                          reply_markup=update_apk_ikb(i18n, apk1, apk2))


@router.callback_query(UpdateApkState.id)
async def get_apk_id(call: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await call.message.delete()
    data_list = call.data.split('_')
    apk = data_list[0]
    id = data_list[1]
    await state.update_data(apk=apk)
    await state.update_data(id=id)
    await state.set_state(UpdateApkState.file)
    
    return call.message.answer(text=i18n.messages.upload_apk())


@router.message(UpdateApkState.file)
async def get_apk1_to_update(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    file = message.document
    if not file:
        return message.answer(text=i18n.messages.is_not_apk_file())
    data: dict = await state.get_data()
    await state.clear()
    apk = data.get('apk')
    id = data.get('id')
    
    if apk == APK1_CALL:
        apk: APK1 = await repository.apk1.update_apk(id=id,
                                                    name=file.file_name,
                                                    file_id=file.file_id)
    elif apk == APK2_CALL:
        apk: APK2 = await repository.apk1.update_apk(id=id,
                                                    name=file.file_name,
                                                    file_id=file.file_id)
    else:
        return message.answer(text=i18n.messages.something_went_wrong())
        
    return message.answer(text=i18n.messages.upload_apk_ok(name=file.file_name))

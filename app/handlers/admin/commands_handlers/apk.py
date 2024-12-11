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
    await state.set_state(LoadApkState.caption_en)
    await state.update_data(apk='apk1')
    
    return message.answer(text=i18n.messages.send_apk_caption_en(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(Command('upload_apk2'))
async def add_apk2(message: Message, i18n: I18nContext,
                          state: FSMContext) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(LoadApkState.caption_en)
    await state.update_data(apk='apk2')
    
    return message.answer(text=i18n.messages.send_apk_caption_en(),
                          reply_markup=abort_command_ikb(i18n))


@router.message(LoadApkState.caption_en)
async def get_apk_caption(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    caption = message.text
    await state.update_data(caption_en=caption)
    await state.set_state(LoadApkState.caption_ua)
    
    return message.answer(text=i18n.messages.send_apk_caption_ua())


@router.message(LoadApkState.caption_ua)
async def get_apk_caption(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    caption = message.text
    await state.update_data(caption_ua=caption)
    await state.set_state(LoadApkState.caption_ru)
    
    return message.answer(text=i18n.messages.send_apk_caption_ru())


@router.message(LoadApkState.caption_ru)
async def get_apk_caption(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    caption = message.text
    await state.update_data(caption_ru=caption)
    await state.set_state(LoadApkState.name)
    
    return message.answer(text=i18n.messages.upload_apk_name())


@router.message(LoadApkState.name)
async def get_apk_name(message: Message, i18n: I18nContext, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(LoadApkState.file)
    return message.answer(text=i18n.messages.upload_apk())


@router.message(LoadApkState.file)
async def get_apk_file(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    file = message.document
    if not file:
        return message.answer(text=i18n.messages.is_not_apk_file())
    data: dict = await state.get_data()
    await state.clear()
    apk = data.get('apk')
    name = data.get('name')
    caption_en = data.get('caption_en')
    caption_ua = data.get('caption_ua')
    caption_ru = data.get('caption_ru')
    if apk == 'apk1':
        await repository.apk1.create_apk(name=name,
                                        file_id=file.file_id,
                                        caption_en=caption_en,
                                        caption_ua=caption_ua,
                                        caption_ru=caption_ru)
    elif apk == 'apk2':
        await repository.apk2.create_apk(name=name,
                                         file_id=file.file_id,
                                         caption_en=caption_en,
                                         caption_ua=caption_ua,
                                         caption_ru=caption_ru)
        
    return message.answer(text=i18n.messages.upload_apk_ok(name=name))


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
    await state.set_state(UpdateApkState.caption_en)
    
    return call.message.answer(text=i18n.messages.send_apk_caption_en())


@router.message(UpdateApkState.caption_en)
async def update_apk_caption(message: Message, i18n: I18nContext, state: FSMContext):
    caption = message.text
    await state.update_data(caption_en=caption)
    await state.set_state(UpdateApkState.caption_ua)
    return message.answer(text=i18n.messages.send_apk_caption_ua())


@router.message(UpdateApkState.caption_ua)
async def update_apk_caption(message: Message, i18n: I18nContext, state: FSMContext):
    caption = message.text
    await state.update_data(caption_ua=caption)
    await state.set_state(UpdateApkState.caption_ru)
    return message.answer(text=i18n.messages.send_apk_caption_ru())


@router.message(UpdateApkState.caption_ru)
async def update_apk_caption(message: Message, i18n: I18nContext, state: FSMContext):
    caption = message.text
    await state.update_data(caption_ru=caption)
    await state.set_state(UpdateApkState.name)
    return message.answer(text=i18n.messages.upload_apk_name())


@router.message(UpdateApkState.name)
async def update_apk_caption(message: Message, i18n: I18nContext, state: FSMContext):
    name = message.text
    if not name:
        return message.answer(text=i18n.messages.upload_apk_name())
    await state.update_data(name=name)
    await state.set_state(UpdateApkState.file)
    return message.answer(text=i18n.messages.upload_apk())


@router.message(UpdateApkState.file)
async def get_apk_to_update(message: Message, i18n: I18nContext,
                       state: FSMContext, repository: Repository):
    file = message.document
    if not file:
        return message.answer(text=i18n.messages.is_not_apk_file())
    data: dict = await state.get_data()
    await state.clear()
    apk = data.get('apk')
    id = data.get('id')
    name = data.get('name')
    caption_en = data.get('caption_en')
    caption_ua = data.get('caption_ua')
    caption_ru = data.get('caption_ru')
    
    if apk == APK1_CALL:
        apk: APK1 = await repository.apk1.update_apk(id=id,
                                                    name=name,
                                                    file_id=file.file_id,
                                                    caption_en=caption_en,
                                                    caption_ua=caption_ua,
                                                    caption_ru=caption_ru)
    elif apk == APK2_CALL:
        apk: APK2 = await repository.apk2.update_apk(id=id,
                                                    name=name,
                                                    file_id=file.file_id,
                                                    caption_en=caption_en,
                                                    caption_ua=caption_ua,
                                                    caption_ru=caption_ru)
    else:
        return message.answer(text=i18n.messages.something_went_wrong())
        
    return message.answer(text=i18n.messages.upload_apk_ok(name=name))

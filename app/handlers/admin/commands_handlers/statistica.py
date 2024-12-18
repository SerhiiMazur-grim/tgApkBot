from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from app.state.admin_state import RefUsersCountState
from app.keyboards.inline_kb.admin_ikb import stata_ikb
from utils import clear_state
from config.callback_data import GET_DB, GET_USERS_IDS_FILE, GET_USERS_BY_REF

if TYPE_CHECKING:
    from services.database import Repository, DBUser


router: Final[Router] = Router(name=__name__)


@router.message(Command('statistica'))
async def get_statistica(message: Message, i18n: I18nContext,
                         state: FSMContext, user: DBUser, repository: Repository):
    await clear_state(state)
    await message.delete()
    stattistica = await repository.user.statistica()
    return message.answer(text=i18n.messages.statistica(total=stattistica.get('total') or 0,
                                                        ref_join=stattistica.get('join_by_ref') or 0,
                                                        prem_users=stattistica.get('prem_users') or 0,
                                                        join_30=stattistica.get('join_30') or 0,
                                                        join_7=stattistica.get('join_7') or 0,
                                                        join_1=stattistica.get('join_1') or 0,),
                          reply_markup=stata_ikb(i18n))
    

@router.callback_query(F.data == GET_DB)
async def get_db_file(call: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await call.answer()
    await clear_state(state)
    return call.message.answer_document(document=FSInputFile(path='apk_bot.db'))


@router.callback_query(F.data == GET_USERS_IDS_FILE)
async def get_users_ids_file(call: CallbackQuery, i18n: I18nContext,
                             state: FSMContext, repository: Repository):
    await call.answer()
    await clear_state(state)
    users_ids = await repository.user.get_all_users_id()
    users_ids = list(map(str, users_ids))
    with open('users_ids.txt', 'w', encoding='utf-8') as f:
        f.writelines(f'{id}\n' for id in users_ids)
    return call.message.answer_document(document=FSInputFile(path='users_ids.txt'))


@router.callback_query(F.data == GET_USERS_BY_REF)
async def get_users_count_by_ref(call: CallbackQuery, i18n: I18nContext,
                             state: FSMContext, repository: Repository):
    await call.answer()
    await clear_state(state)
    await state.set_state(RefUsersCountState.ref_url)
    return call.message.answer(text=i18n.messages.send_ref_url())


@router.message(RefUsersCountState.ref_url)
async def get_ref_url(message: Message, i18n: I18nContext, state: FSMContext, repository: Repository):
    url = message.text
    if not url:
        return message.answer(text=i18n.messages.is_not_ref_url())
    if 'start=' not in url:
        return message.answer(text=i18n.messages.is_not_ref_url())
    
    ref = url.split('=')[-1]
    users_count = await repository.user.ref_count(ref)
    await state.clear()
    if not users_count:
        return message.answer(text=i18n.messages.no_users_by_ref())
    return message.answer(text=i18n.messages.users_count_by_ref(users_count=users_count))

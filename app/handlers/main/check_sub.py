from __future__ import annotations

from typing import Any, Final, TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from config.callback_data import CHECK_SUB
from app.keyboards.inline_kb.user_ikb import apk_files_ikb, galery_ikb
from app.filters import PrivateChatFilter
from app.state.user_state import CatalogState
from utils import clear_state, is_subscribe, check_sub
from app.dialogs.user_dialogs import CatalogDialog

if TYPE_CHECKING:
    from services.database import DBUser, Repository


router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == CHECK_SUB)
async def check_user_sub(call: CallbackQuery, bot: Bot, i18n: I18nContext,
                        user: DBUser, repository: Repository):
    await check_sub(call, bot, i18n, user, repository)

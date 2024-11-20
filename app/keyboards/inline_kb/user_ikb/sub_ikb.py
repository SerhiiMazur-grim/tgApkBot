from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import ABORT_COMMAND
from services.database import SubChannel


def channel_list_to_sub_ikb(i18n: I18nContext, data: List[SubChannel]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in data:
        ikb.button(text=i.username, url=i.invate_url)
    ikb.adjust(1)
    
    return ikb.as_markup()

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import REF_START
from services.database import SubChannel


def ref_st_ikb(btn_text) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text=btn_text, callback_data=REF_START)
    ikb.adjust(1)
    
    return ikb.as_markup()

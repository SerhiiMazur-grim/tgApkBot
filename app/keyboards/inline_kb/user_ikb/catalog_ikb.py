from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import NEXT, PREV
from services.database import SubChannel


def galery_ikb(page, pages) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text='⬅️', callback_data=PREV)
    ikb.button(text=f'{page}/{pages}', callback_data='TEST')
    ikb.button(text='➡️', callback_data=NEXT)
    ikb.adjust(3)
    
    return ikb.as_markup()

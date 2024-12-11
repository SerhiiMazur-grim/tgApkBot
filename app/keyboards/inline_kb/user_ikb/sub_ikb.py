from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import CHECK_SUB
from services.database import SubChannel


def channel_list_to_sub_ikb(i18n: I18nContext, data: List[SubChannel]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    num = 1
    for i in data:
        ikb.button(text=i18n.ik_button.subscribe(num=num), url=i.invate_url)
        num += 1
    ikb.button(text=i18n.ik_button.check_sub(), callback_data=CHECK_SUB)
    ikb.adjust(1)
    
    return ikb.as_markup()

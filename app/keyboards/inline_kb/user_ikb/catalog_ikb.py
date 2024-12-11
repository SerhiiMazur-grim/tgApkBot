from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.settings import Settings
from config.callback_data import NEXT, PREV, DELL, CLOSE_CATALOG
from services.database import SubChannel


settings = Settings()


def galery_ikb(page, pages, user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text='⬅️', callback_data=PREV)
    ikb.button(text=f'{page}/{pages}', callback_data='TEST')
    ikb.button(text='➡️', callback_data=NEXT)
    if user_id == settings.admin_chat_id:
        ikb.button(text='DELLETE', callback_data=DELL)
    ikb.button(text='Close', callback_data=CLOSE_CATALOG)
    ikb.adjust(3,1)
    
    return ikb.as_markup()

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import ABORT_COMMAND
from services.database import RefMessage


def abort_command_ikb(i18n: I18nContext, language: str = None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    if language:
        ikb.button(text=i18n.core.get('ik_button-abort', language), callback_data=ABORT_COMMAND)
    else:
        ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()


def del_sub_channel_ikb(i18n: I18nContext, data: List[RefMessage]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in data:
        ikb.button(text=i.username, callback_data=str(i.id))
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()


def del_ref_ikb(i18n: I18nContext, data: List[RefMessage]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in data:
        ikb.button(text=i.ref, callback_data=str(i.id))
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()

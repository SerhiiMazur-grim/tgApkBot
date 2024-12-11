from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import ABORT_COMMAND, APK_1, APK_2
from services.database import SubChannel


def apk_files_ikb(i18n: I18nContext, apk1: str, apk2: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text=apk1, callback_data=APK_1)
    ikb.button(text=apk2, callback_data=APK_2)
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()

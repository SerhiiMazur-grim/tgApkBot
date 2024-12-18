from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from config.callback_data import (
    ABORT_COMMAND,
    APK1_CALL,
    APK2_CALL,
    SEND_POST,
    GET_DB,
    GET_USERS_IDS_FILE,
    GET_USERS_BY_REF
)
from services.database import RefMessage, APK1, APK2


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


def update_apk_ikb(i18n: I18nContext, apk1: APK1, apk2: APK2) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text=apk1.name, callback_data=f'{APK1_CALL}_{apk1.id}')
    ikb.button(text=apk2.name, callback_data=f'{APK2_CALL}_{apk2.id}')
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()


def send_post_ikb(i18n: I18nContext) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text='SEND', callback_data=SEND_POST)
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()


def choose_cat_ikb(i18n: I18nContext, data: list[tuple]):
    ikb = InlineKeyboardBuilder()
    for title, id in data:
        ikb.button(text=title, callback_data=str(id))
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(1)
    
    return ikb.as_markup()


def stata_ikb(i18n: I18nContext) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text=i18n.ik_button.get_db(), callback_data=GET_DB)
    ikb.button(text=i18n.ik_button.get_users_ids_file(), callback_data=GET_USERS_IDS_FILE)
    ikb.button(text=i18n.ik_button.get_users_by_ref(), callback_data=GET_USERS_BY_REF)
    ikb.button(text=i18n.ik_button.abort(), callback_data=ABORT_COMMAND)
    ikb.adjust(2, 1)
    
    return ikb.as_markup()

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram_i18n import I18nContext


def back_to_main_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=i18n.button.back_to_main_rkb())
    kb.adjust(1)
    
    return kb.as_markup(resize_keyboard=True)
    
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram_i18n import I18nContext


def main_keyboard(i18n: I18nContext, language: str | None = None) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    
    if language:
        kb.button(text=i18n.core.get('button-get_apk', language))
        kb.button(text=i18n.core.get('button-galery', language))
    else:
        kb.button(text=i18n.button.get_apk())
        kb.button(text=i18n.button.galery())
    
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
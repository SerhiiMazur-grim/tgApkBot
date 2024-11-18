from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n.context import I18nContext


@dataclass
class Window:
    message_key: str
    key_board: InlineKeyboardMarkup
    
    def caption(self, i18n: I18nContext) -> str:
        locale: str = i18n.locale
        return i18n.core.get(self.message_key, locale)

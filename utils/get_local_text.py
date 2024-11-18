from aiogram_i18n.context import I18nContext


def get_text(i18n: I18nContext, message_key: str) -> str:
        locale: str = i18n.locale
        return i18n.core.get(message_key, locale)

from aiogram import Bot, Dispatcher

from base.factories import create_bot, create_dispatcher
from base.runners import run_polling, run_webhook
from config.settings import Settings
from utils.loggers import setup_logger


def main():
    setup_logger()
    settings: Settings = Settings()
    dp: Dispatcher = create_dispatcher(settings=settings)
    bot: Bot = create_bot(settings=settings)

    if settings.use_webhook:
        return run_webhook(dispatcher=dp, bot=bot, settings=settings)
    return run_polling(dispatcher=dp, bot=bot)


if __name__ == '__main__':
    main()

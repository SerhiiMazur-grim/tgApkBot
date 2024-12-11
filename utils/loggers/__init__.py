import logging

from config.settings import Settings
from .multiline import MultilineLogger

__all__ = ["database", "webhook", "setup_logger", "MultilineLogger"]

webhook: logging.Logger = logging.getLogger("bot.webhook")
database: logging.Logger = logging.getLogger("bot.database")


settings = Settings()


def setup_logger(level: int = logging.INFO) -> None:
    logging_info = settings.logging_info
    # filename = settings.logs_to_file
    filename = None
    
    if not logging_info:
        level = logging.WARNING
    
    for name in ["aiogram.middlewares", "aiogram.event", "aiohttp.access"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.basicConfig(
        filename=filename,
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
    )

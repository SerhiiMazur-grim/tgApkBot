import os
import logging
from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.types import Message

if TYPE_CHECKING:
    from services.database import DBUser


async def is_subbscribe(bot: Bot, user: DBUser) -> bool:
    pass

from __future__ import annotations

from typing import Final

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config.callback_data import ABORT_COMMAND
from utils import clear_state


router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == ABORT_COMMAND)
async def abort_command(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await clear_state(state)

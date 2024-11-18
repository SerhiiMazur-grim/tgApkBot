from typing import Final

from aiogram import Router

from . import (
    start,
    change_language,
    back_to_main_menu
)

router: Final[Router] = Router(name=__name__)

router.include_routers(start.router,
                       change_language.router,
                       back_to_main_menu.router)

from typing import Final

from aiogram import Router


from . import (
    back_to_main_menu,
    main_menu
)

router: Final[Router] = Router(name=__name__)

router.include_routers(back_to_main_menu.router,
                       main_menu.router,
                       )
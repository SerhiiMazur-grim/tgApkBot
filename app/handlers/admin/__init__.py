from typing import Final

from aiogram import Router

from .commands_handlers import image_id, abort_command, sub_channels


router: Final[Router] = Router(name=__name__)
router.include_routers(image_id.router, abort_command.router, sub_channels.router)

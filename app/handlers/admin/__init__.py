from typing import Final

from aiogram import Router

from .commands_handlers import (
    image_id,
    abort_command,
    sub_channels,
    add_image,
    ref_start_message,
    apk,
    send_post,
    category
)


router: Final[Router] = Router(name=__name__)

router.include_routers(
    image_id.router,
    abort_command.router,
    sub_channels.router,
    add_image.router,
    ref_start_message.router,
    apk.router,
    send_post.router,
    category.router
)

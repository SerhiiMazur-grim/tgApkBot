from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, List

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from services.database import SubChannel
from app.filters import PrivateChatFilter
from app.state.admin_state import AddImgToGalery
from app.keyboards.inline_kb.admin_ikb import abort_command_ikb, choose_cat_ikb
from utils import clear_state

if TYPE_CHECKING:
    from services.database import Repository, DBUser


router: Final[Router] = Router(name=__name__)


@router.message(Command('add_image_to_galery'))
async def start_add_img_to_galery(message: Message, i18n: I18nContext,
                                  state: FSMContext,
                                  user: DBUser,
                                  repository: Repository) -> TelegramMethod[Any]:
    await message.delete()
    await state.set_state(AddImgToGalery.cat)
    locale = user.locale
    categories = await repository.category.get_titles_and_id(locale)
    return message.answer(text=i18n.messages.choose_cat_for_upload_image(),
                          reply_markup=choose_cat_ikb(i18n, categories))
    
    
    
    # return message.answer(text=i18n.messages.send_me_images())


@router.message(AddImgToGalery.img)
async def collect_images(message: Message, bot: Bot, i18n: I18nContext,
                         state: FSMContext, album: List[Message] | None,
                         repository: Repository) -> TelegramMethod[Any]:
    await clear_state(state)
    
    if album:
        img_ids = []
        for msg in album:
            img_id = msg.photo[-1].file_id
            img_ids.append(img_id)
        await repository.galery.create_images(img_ids)
        chat_id = album[0].from_user.id
        return await bot.send_message(chat_id=chat_id, text=i18n.messages.imgs_added())
    
    else:
        img_id = message.photo[-1].file_id
        await repository.galery.create_image(img_id)
        return message.answer(text=i18n.messages.imgs_added())

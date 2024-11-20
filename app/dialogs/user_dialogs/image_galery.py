from typing import Any, Final, TYPE_CHECKING

from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config.callback_data import NEXT, PREV, DELL
from app.keyboards.inline_kb.user_ikb import galery_ikb
from services.database import Repository


class CatalogDialog():
        
    def __init__(self, call: CallbackQuery,
                 state: FSMContext, repository: Repository) -> None:
        self.call = call
        self.state = state
        self.repository = repository
    
    @property
    def call_data(self):
        data: str = self.call.data
        return data
    
    async def state_data(self):
        data: dict = await self.state.get_data()
        return data
    
    async def dell_img(self):
        img_id = 0
        await self.repository.galery.delete_image(img_id)
        data = await self.state_data()
        catalog = data.get('catalog')
        pages = data.get('pages')
        pages -= 1
        page = data.get('page')
        catalog.pop(page-1)
        
        await self.state.update_data({
            'catalog': catalog,
            'pages': pages
        })
        return await self._next_step()
    
    
    async def _next_step(self):
        data = await self.state_data()
        catalog = data.get('catalog')
        pages = data.get('pages')
        page = data.get('page')
        next_page = page+1
        index = page
        if next_page>pages:
            next_page = 1
            index = 0
            
        await self.state.update_data({
            'page': next_page
        })
        media = InputMediaPhoto(media=catalog[index])
        return await self.call.message.edit_media(media=media,
                                                  reply_markup=galery_ikb(next_page, pages))
    
    
    async def _prev_step(self):
        data = await self.state_data()
        catalog = data.get('catalog')
        pages = data.get('pages')
        page = data.get('page')
        prev_page = page-1
        index = page-2
        if prev_page < 1:
            prev_page = pages
            index = pages-1
        await self.state.update_data({
            'page': prev_page
        })
        media = InputMediaPhoto(media=catalog[index])
        return await self.call.message.edit_media(media=media,
                                                  reply_markup=galery_ikb(prev_page, pages))
    
    
    async def dialog_window(self):
        
        if self.call_data == DELL:
            return await self.dell_img()
        
        if self.call_data == NEXT:
            return await self._next_step()
        
        if self.call_data == PREV:
            return await self._prev_step()

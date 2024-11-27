from typing import Any, Final, TYPE_CHECKING

from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from config.callback_data import NEXT, PREV, DELL, CLOSE_CATALOG
from app.keyboards.inline_kb.user_ikb import galery_ikb
from services.database import Repository
from utils import clear_state


class CatalogDialog():
        
    def __init__(self, call: CallbackQuery,
                 state: FSMContext, repository: Repository, user_id: int) -> None:
        self.call = call
        self.state = state
        self.repository = repository
        self.user_id = user_id
    
    @property
    def call_data(self):
        data: str = self.call.data
        return data
    
    async def state_data(self):
        data: dict = await self.state.get_data()
        return data
    
    async def dell_img(self):
        img_id = 0
        data = await self.state_data()
        catalog = data.get('catalog')
        pages = data.get('pages')
        pages -= 1
        page = data.get('page')
        index = page-1
        await self.repository.galery.delete_image(catalog[index])
        catalog.pop(index)
        if not catalog:
            return await self.close_window()
        
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
        if pages == 1:
            return
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
                                                  reply_markup=galery_ikb(next_page, pages, self.user_id))
    
    
    async def _prev_step(self):
        data = await self.state_data()
        catalog = data.get('catalog')
        pages = data.get('pages')
        page = data.get('page')
        if pages == 1:
            return
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
                                                  reply_markup=galery_ikb(prev_page, pages, self.user_id))
    
    
    async def close_window(self):
        await clear_state(self.state)
        await self.call.message.delete()
    
    
    async def dialog_window(self):
        
        if self.call_data == CLOSE_CATALOG:
            return await self.close_window()
        
        if self.call_data == DELL:
            return await self.dell_img()
        
        if self.call_data == NEXT:
            return await self._next_step()
        
        if self.call_data == PREV:
            return await self._prev_step()

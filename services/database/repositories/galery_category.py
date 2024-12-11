from typing import Optional, cast, List

from aiogram import Bot
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import GaleryCategory
from .base import BaseRepository


class CategoryRepository(BaseRepository):
    
    async def get(self, id: int | str) -> Optional[GaleryCategory]:
        id = int(id)
        return cast(
            Optional[GaleryCategory],
            await self._session.scalar(select(GaleryCategory).where(GaleryCategory.id == id)),
        )
    
    
    async def get_all_categories(self) -> list[GaleryCategory]:
        result = await self._session.scalars(select(GaleryCategory))
        return result.all()
    
    
    async def get_titles_and_id(self, local: str):
        if local == 'ru':
            rez = await self._session.execute(select(GaleryCategory.title_ru, GaleryCategory.id))
        elif local == 'uk':
            rez = await self._session.execute(select(GaleryCategory.title_ua, GaleryCategory.id))
        else:
            rez = await self._session.execute(select(GaleryCategory.title_en, GaleryCategory.id))
        return rez.all()
    
    
    async def get_cat_images(self, id: int | str) -> List[str]:
        id = int(id)
        rez = await self._session.scalars(select(GaleryCategory.images).where(GaleryCategory.id==id))
        return rez.all()
        

    async def create_category(self, title: list[str]) -> GaleryCategory:
        cat: GaleryCategory = GaleryCategory(title_en=title[0],
                                             title_ua=title[1],
                                             title_ru=title[2])
        await self.commit(cat)
        return cat
    
    
    async def delete_category(self, cat_id: str | int) -> None:
        cat_id = int(cat_id)
        # rez = await self._session.execute(
        #     delete(GaleryCategory).where(GaleryCategory.id == cat_id).returning(GaleryCategory)
        # )
        # deleted_cat = rez.scalars().first()
        # await self.commit()
        # return deleted_cat.title_ua
        category = await self._session.get(GaleryCategory, cat_id)
        if category:
            await self._session.delete(category)
            await self.commit()
            return category.title_ua
        return None

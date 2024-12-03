from typing import Optional, cast, List

from aiogram import Bot
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import GaleryCategory
from .base import BaseRepository


class CategoryRepository(BaseRepository):
    
    async def get(self, id: int) -> Optional[GaleryCategory]:
        return cast(
            Optional[GaleryCategory],
            await self._session.scalar(select(GaleryCategory).where(GaleryCategory.id == id)),
        )
    
    
    async def get_all_categories(self) -> list[GaleryCategory]:
        result = await self._session.scalars(select(GaleryCategory))
        return result.all()
    
    
    async def get_cat_images(self, id: int | str) -> List[str]:
        id = int(id)
        rez = await self._session.scalars(select(GaleryCategory.images).where(GaleryCategory.id==id))
        return rez.all()
        

    async def create_category(self, title: str) -> GaleryCategory:
        cat: GaleryCategory = GaleryCategory(title=title)
        await self.commit(cat)
        return cat
    
    
    async def create_categories(self, titles: list[str]) -> list[GaleryCategory]:
        categoris = [GaleryCategory(title=title) for title in titles]
        self._session.add_all(categoris)
        await self._session.commit()
        return categoris
    
    
    async def delete_category(self, cat_id: str | int) -> None:
        cat_id = int(cat_id)
        rez = await self._session.execute(
            delete(GaleryCategory).where(GaleryCategory.id == cat_id).returning(GaleryCategory)
        )
        deleted_cat = rez.scalars().first()
        await self.commit()
        return deleted_cat.title
        

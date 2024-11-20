from typing import Optional, cast, List

from aiogram import Bot
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import Galery
from .base import BaseRepository


class GaleryRepository(BaseRepository):
    
    async def get(self, img_id: int) -> Optional[Galery]:
        return cast(
            Optional[Galery],
            await self._session.scalar(select(Galery).where(Galery.img_id == img_id)),
        )
    
    
    async def get_all_images(self) -> list[Galery]:
        result = await self._session.scalars(select(Galery))
        return result.all()
    
    
    async def get_all_image_ids(self) -> List[str]:
        rez = await self._session.scalars(select(Galery.img_id))
        return rez.all()
        

    async def create_image(self, img_id: str) -> Galery:
        image: Galery = Galery(img_id = img_id)
        await self.commit(image)
        return image
    
    
    async def create_images(self, img_ids: list[str]) -> list[Galery]:
        images = [Galery(img_id=img_id) for img_id in img_ids]
        self._session.add_all(images)
        await self._session.commit()
        return images
    
    
    async def delete_image(self, img_id: str) -> None:
        await self._session.execute(
            delete(Galery).where(Galery.img_id == img_id)
        )
        await self.commit()
        

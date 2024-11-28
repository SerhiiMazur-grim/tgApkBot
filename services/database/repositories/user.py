from typing import Optional, cast

from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )
    
    async def get_all_users(self) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalars(select(DBUser)),
        )
    
    async def get_active_users(self) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalars(select(DBUser).where(DBUser.active == True)),
        )
    
    
    async def get_all_users_id(self):
        rez = await self._session.scalars(select(DBUser.id))
        return rez.all()
    
    
    async def get_referal_users(self, referal: str) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalars(select(DBUser).where(DBUser.referal == referal)),
        )


    async def create_from_telegram(self, user: User, locale: str,
                                   referal: str | None, chat: Chat) -> DBUser:
        
        user_name = user.full_name
        if not user_name:
            user_name = '😎'
        
        db_user: DBUser = DBUser(
            id=user.id,
            name=user.full_name,
            chat_type=chat.type,
            premium=user.is_premium,
            referal=referal,
            locale=locale,
        )

        await self.commit(db_user)
        return db_user
    
    
    async def update_user_subscribe(self, user: DBUser, subscribe = True):
        user.subscribe = subscribe
        await self.commit(user)
    
    
    async def update_user_active(self, user_id: int, active: bool):
        user: DBUser = await self.get(user_id)
        user.active = active
        await self.commit(user)
    
    
    async def delete_user(self, user_id):
        user_id = int(user_id)
        rez = await self._session.execute(
            delete(DBUser).where(DBUser.id == user_id).returning(DBUser)
        )
        deleted_user = rez.scalars().first()
        await self.commit()
        return deleted_user.name

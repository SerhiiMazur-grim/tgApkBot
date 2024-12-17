from typing import Optional, cast
from datetime import timedelta, datetime

from aiogram.enums import ChatType
from aiogram.types import Chat, User
from sqlalchemy import select, update, values, delete

from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int|str) -> Optional[DBUser]:
        user_id = int(user_id)
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
    
    
    async def get_user_local(self, id:int|str):
        id = int(id)
        locale = await self._session.scalar(select(DBUser.locale).where(DBUser.id==id))
        return locale


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
    
    
    async def statistica(self):
        time_now = datetime.now()
        d30 = time_now - timedelta(days=30)
        d7 = time_now - timedelta(days=7)
        d1 = time_now - timedelta(days=1)
        
        total_users = await self._session.scalars(select(DBUser))
        total_users = total_users.all()
        
        prem_users = await self._session.scalars(select(DBUser).where(DBUser.premium == 1))
        prem_users = prem_users.all()
        
        join_30 = await self._session.scalars(select(DBUser).where(DBUser.created_at > d30))
        join_30 = join_30.all()
        
        join_7 = await self._session.scalars(select(DBUser).where(DBUser.created_at > d7))
        join_7 = join_7.all()
        
        join_1 = await self._session.scalars(select(DBUser).where(DBUser.created_at > d1))
        join_1 = join_1.all()
        
        join_by_ref = await self._session.scalars(select(DBUser).where(DBUser.referal != None))
        join_by_ref = join_by_ref.all()
        
        stata = {
        'total' : len(total_users),
        'join_by_ref' : len(join_by_ref),
        'prem_users' : len(prem_users),
        'join_30' : len(join_30),
        'join_7' : len(join_7),
        'Join_1' : len(join_1),
        }
        return stata
    
    
    async def ref_count(self, ref: str):
        rez = await self._session.scalars(select(DBUser).where(DBUser.referal == ref))
        return len(rez.all())

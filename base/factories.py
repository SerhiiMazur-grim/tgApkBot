from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import ConnectionPool, Redis

from enums import Locale
from middlewares import (
    DBSessionMiddleware,
    RetryRequestMiddleware,
    UserManager,
    UserMiddleware,
    ForbiddenErrorMiddleware,
    AlbumMiddleware
)
from services.database import create_pool
from app.handlers import main, user, admin
from utils import msgspec_json as mjson
from config.settings import Settings


def _setup_outer_middlewares(dispatcher: Dispatcher, settings: Settings) -> None:
    pool = dispatcher["session_pool"] = create_pool(
        dsn=settings.build_sqlite_dsn(), enable_logging=settings.sqlalchemy_logging
    )
    i18n_middleware = dispatcher["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(
            path="translations/{locale}",
            raise_key_error=False,
            locales_map={Locale.RU: Locale.UK, Locale.UK: Locale.EN},
        ),
        manager=UserManager(),
        default_locale=Locale.DEFAULT,
    )

    dispatcher.update.outer_middleware(ForbiddenErrorMiddleware())
    dispatcher.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dispatcher.update.outer_middleware(UserMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.message.middleware(AlbumMiddleware())


def create_dispatcher(settings: Settings) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_database,
        )
    )
    
    memory_storage: MemoryStorage = MemoryStorage()
    
    if settings.use_redis:
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode)
    else:
        storage=memory_storage
        redis=None

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=storage,
        redis=redis,
        settings=settings,
    )
    
    dispatcher.include_routers(
        main.router,
        admin.router,
        user.router
    )
    
    _setup_outer_middlewares(dispatcher=dispatcher, settings=settings)
    _setup_inner_middlewares(dispatcher=dispatcher)
    
    return dispatcher


# def create_bot(settings: Settings) -> Bot:
#     """
#     :return: Configured ``Bot`` with retry request middleware
#     """
#     session: AiohttpSession = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
#     session.middleware(RetryRequestMiddleware())
#     return Bot(
#         token=settings.bot_token.get_secret_value(),
#         parse_mode=ParseMode.HTML,
#         session=session,
#     )

def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

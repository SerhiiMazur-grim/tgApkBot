from aiogram.fsm.state import State, StatesGroup


class CatalogState(StatesGroup):
    catalog = State()
    pages = State()
    page = State()

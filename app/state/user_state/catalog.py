from aiogram.fsm.state import State, StatesGroup


class CatalogState(StatesGroup):
    category = State()
    catalog = State()
    pages = State()
    page = State()

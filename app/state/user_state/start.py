from aiogram.fsm.state import State, StatesGroup


class UserRefStartState(StatesGroup):
    ref = State()
    answer = State()

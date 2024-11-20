from aiogram.fsm.state import State, StatesGroup


class GetImageIdState(StatesGroup):
    image = State()


class GetChannelUsernameState(StatesGroup):
    username = State()
    invate_url = State()


class DelSubChannelState(StatesGroup):
    id = State()


class AddImgToGalery(StatesGroup):
    img = State()

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


class GetRefStartState(StatesGroup):
    ref = State()
    en = State()
    ua = State()
    ru = State()


class DelRefStartState(StatesGroup):
    id = State()


class LoadApkState(StatesGroup):
    apk = State()
    file = State()


class UpdateApkState(StatesGroup):
    apk = State()
    id = State()
    file = State()
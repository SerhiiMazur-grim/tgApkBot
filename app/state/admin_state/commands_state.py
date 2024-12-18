from aiogram.fsm.state import State, StatesGroup


class GetImageIdState(StatesGroup):
    image = State()


class GetChannelUsernameState(StatesGroup):
    username = State()
    invate_url = State()


class DelSubChannelState(StatesGroup):
    id = State()


class AddImgToGalery(StatesGroup):
    cat = State()
    img = State()


class AddCategoryState(StatesGroup):
    cat = State()


class DellCategoryState(StatesGroup):
    cat = State()


class GetRefStartState(StatesGroup):
    ref = State()
    img = State()
    en = State()
    ua = State()
    ru = State()
    btn_en = State()
    btn_ua = State()
    btn_ru = State()
    answer_en = State()
    answer_ua = State()
    answer_ru = State()


class DelRefStartState(StatesGroup):
    id = State()


class LoadApkState(StatesGroup):
    apk = State()
    caption_en = State()
    caption_ua = State()
    caption_ru = State()
    name = State()
    file = State()


class UpdateApkState(StatesGroup):
    apk = State()
    id = State()
    caption_en = State()
    caption_ua = State()
    caption_ru = State()
    name = State()
    file = State()


class PostState(StatesGroup):
    media = State()
    post = State()
    send = State()


class RefUsersCountState(StatesGroup):
    ref_url = State()

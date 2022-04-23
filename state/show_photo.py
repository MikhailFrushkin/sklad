from aiogram.dispatcher.filters.state import StatesGroup, State


class Showphoto(StatesGroup):
    show_qr = State()
    show_all = State()


class Place(StatesGroup):
    mesto_1 = State()
    mesto_2 = State()
    mesto_3 = State()
    mesto_4 = State()
    dowl = State()
    dowload = State()


class Search(StatesGroup):
    sklad = State()
    art = State()
    show_all = State()

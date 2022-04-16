from aiogram.dispatcher.filters.state import StatesGroup, State


class Showphoto(StatesGroup):
    show_qr = State()
    show_all = State()
    graf = State()


class Place(StatesGroup):
    mesto_1 = State()
    mesto_2 = State()
    mesto_3 = State()
    mesto_4 = State()
    mesto_5 = State()
from aiogram.dispatcher.filters.state import StatesGroup, State


class Showphoto(StatesGroup):
    show_qr = State()
    show_all = State()

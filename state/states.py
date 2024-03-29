from aiogram.dispatcher.filters.state import StatesGroup, State


class EditKeyboard(StatesGroup):
    edit = State()


class Showphoto(StatesGroup):
    show_qr = State()
    show_all = State()


class Logging(StatesGroup):
    log = State()


class QR(StatesGroup):
    qr = State()


class Messages(StatesGroup):
    mes = State()


class Place(StatesGroup):
    mesto_1 = State()
    mesto_2 = State()
    mesto_3 = State()
    mesto_4 = State()
    dowload = State()


class Search(StatesGroup):
    search_name = State()


class Orders(StatesGroup):
    order = State()


class Stock(StatesGroup):
    group = State()
    nums = State()
    show_stock = State()
    order = State()
    min_vitrina = State()


class Action(StatesGroup):
    set_group = State()
    set_num = State()
    show_product = State()


class Verification(StatesGroup):
    get_groups = State()
    view_result = State()
    get_list = State()
    check_item = State()
    edited_status = State()
    edited_status_art = State()


class Graf(StatesGroup):
    check_graf = State()
    day_graf = State()


class NewProducts(StatesGroup):
    choice_ds = State()
    choice_ds_f = State()
    choice_tg = State()
    show_products = State()
    show_products_f = State()
    show_new_products = State()
    show_new_products_f = State()


class DowloadNewProducts(StatesGroup):
    choice_dowload = State()


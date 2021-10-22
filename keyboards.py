from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard():
    start_keyboard = InlineKeyboardMarkup()
    search_button = InlineKeyboardButton(text='Поиск по городу', callback_data='search')
    source_codes = InlineKeyboardButton(text='Исходный код', callback_data='source')
    start_keyboard.add(search_button)
    start_keyboard.add(source_codes)
    return start_keyboard


def get_source_keyboard():
    source_keyboard = InlineKeyboardMarkup()
    search_button = InlineKeyboardButton(text='Поиск по городу', callback_data='search')
    source_keyboard.add(search_button)
    return source_keyboard


def city_list_generator(city_list):
    city_list_keyboard = InlineKeyboardMarkup()
    for city in city_list:
        city_data = city.split(':')
        some_city_button = InlineKeyboardButton(text=city_data[0], callback_data=f'd_{city_data[1]}')
        city_list_keyboard.add(some_city_button)
    return city_list_keyboard


def search_options(destination_id):
    search_options_keybord = InlineKeyboardMarkup()
    hight_price = InlineKeyboardButton(text='Дорогие', callback_data=f"s_1_{destination_id}")
    low_price = InlineKeyboardButton(text='Дешевые', callback_data=f"s_2_{destination_id}")
    from_center_low = InlineKeyboardButton(text='Дешевые в центре', callback_data=f"s_3_{destination_id}")
    from_center_hight = InlineKeyboardButton(text='Дорогие в центре', callback_data=f"s_4_{destination_id}")
    cancel = InlineKeyboardButton(text='Отмена', callback_data=f"cancel")
    search_options_keybord.row(hight_price, low_price)
    search_options_keybord.add(from_center_hight)
    search_options_keybord.add(from_center_low)
    search_options_keybord.add(cancel)
    return search_options_keybord


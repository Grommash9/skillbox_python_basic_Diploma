import asyncio

import aiogram
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo, InputMediaPhoto
from hotel import Hotel

from city import City
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


def destination_id_finder(city):
    url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

    querystring = {"locale": "ru_RU", "currency": "UAH", "query": city}

    headers = {
        'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
        'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_shit = response.json()

    try:
        result_dict = dict(json_shit)

        results = []

        for citys in result_dict["suggestions"][0]['entities']:
            results.append(City(citys))

        return results

    except KeyError:
        return 'Город не найден'


def hotel_finder(destinationID, user_ID):

    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

    querystring = {"currency": "UAH", "locale": "ru_RU", "adults_number": "1", "sort_order": "PRICE",
                   "destination_id": destinationID, "checkout_date": "2022-03-27", "checkin_date": "2022-03-26"}

    headers = {
        'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
        'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_shit = response.json()

    hotels_list = []

    for hotel in json_shit['searchResults']['results']:
        hotels_list.append(Hotel(hotel))


    for hotels in hotels_list:
        result = str(hotels.id) + str(hotels.name) + str(hotels.streetAddress) + str(hotels.ratePlan) + str(hotels.ratePlan_info)
        print(result)
        #hotels.get_photos(hotels.id)

    print(response.text)




bot = Bot(token='1975741586:AAFJQilNIPrGBoDBLZ450uVNTtx8jw6PaU4')
dp = Dispatcher(bot)


@dp.message_handler()
async def process_start_command(message: types.Message):
    print('от кого', message.from_user)

    results_1 = destination_id_finder(message.text)
    if results_1 == 'Город не найден':
        await message.reply(text='Город не найден')
    else:
        buttons_list = []
        for city in results_1:
            x = InlineKeyboardButton(text=city.caption, callback_data=f'destinationId/{city.destinationId}/{message.from_user.id}')
            buttons_list.append(x)
        inline_kb_full = InlineKeyboardMarkup()
        for buttons in buttons_list:
            inline_kb_full.add(buttons)
        await message.reply(text='Выберите наиболее подходящий вариант: ', reply_markup=inline_kb_full)


@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    lists = callback_query.data.split('/')
    hotel_finder(int(lists[1]), int(lists[2]))


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)

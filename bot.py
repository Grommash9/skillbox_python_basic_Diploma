from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
import logging

from aiogram.utils.exceptions import InvalidQueryID

import config
import keyboards
import rapid_api


class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()


logging.basicConfig(level=logging.INFO)
memory_storage = MemoryStorage()
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot, storage=memory_storage)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в бот, по подбору отелей.', reply_markup=keyboards.get_start_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'search')
async def handle_a(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Отправьте название города для поиска на русском языке, для отмены отправьте один любой символ")
    await InputUserData.step_1.set()
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def questionnaire_state_1_message(message: types.Message, state: FSMContext):
    async with state.proxy() as user_data:
        user_data['input_user'] = message.text
        await state.finish()
    if len(user_data['input_user']) != 1:
        city_list = rapid_api.get_destination_id(user_data['input_user'])
        if len(city_list) == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"К сожалнию по запросу {user_data['input_user']} ничего не найдено",
                                   reply_markup=keyboards.get_start_keyboard())
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Пожалуйста нажмите на наиболее подходящий вариант: ',
                                   reply_markup=keyboards.city_list_generator(city_list))
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Вы отменили операцию: ', parse_mode="Markdown", reply_markup=keyboards.get_start_keyboard())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('d_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Пожалуйста выбирите опцию: ',
                           reply_markup=keyboards.search_options(callback_query.data[2:]))
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('s_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    hotels_dict = rapid_api.get_hotels(destination_id=data[2], option=data[1])
    if len(hotels_dict) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='К сожалению отелей по вашему запросу не найдено',
                               reply_markup=keyboards.get_start_keyboard())
    else:
        for hotel_id, hotel_data in hotels_dict.items():
            currect_photo_link = hotel_data['photo'].split('?')[0]
            caption_message = ''
            for keys, data in hotel_data.items():
                if keys != 'photo' and keys != 'exactCurrent':
                    caption_message += f"{data}\n\n"
            await bot.send_photo(chat_id=callback_query.from_user.id, photo=currect_photo_link, caption=caption_message)
    try:
        await bot.answer_callback_query(callback_query.id)
    except InvalidQueryID:
        pass


@dp.callback_query_handler(lambda c: c.data == 'source')
async def handle_source(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="https://github.com/Grommash9/skillbox_python_basic_Diploma", reply_markup=keyboards.get_source_keyboard())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def handle_cancel(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Вы отменили операцию", reply_markup=keyboards.get_start_keyboard())
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(dp)

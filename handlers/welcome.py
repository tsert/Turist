from datetime import date, timedelta

import telebot

from config_data import config
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar
from loguru import logger

import hotels_api
from users import User


TOKEN = config.BOT_TOKEN
bot = telebot.TeleBot(TOKEN)

# logger.add(sink="logs/debug.log", format=config.LOG_FORMAT, level=config.LOG_LEVEL, diagnose=True, backtrace=False,
#            rotation="500 kb", retention=3, compression="zip")
logger.add('logs/debug.log', format='{time} {level} {message}')


def set_city_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isalpha():
        msg = bot.send_message(chat_id, 'Название  должно содержать только буквы')
        bot.register_next_step_handler(msg, set_city_step)
    else:
        user.city = message.text
        user.city_id = hotels_api.get_city_id(user.city)
        if user.city_id is None:
            msg = bot.send_message(chat_id, 'Город не найден. Проверьте правильность ввода')
            bot.register_next_step_handler(msg, set_city_step)

        else:
            set_check_in(message)


def set_check_in(message: types.Message) -> None:
    chat_id = message.chat.id
    # user = users.user_data[chat_id]
    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today(), locale='ru').build()
    bot.send_message(chat_id, 'выберите дату заезда', reply_markup=calendar)


def set_check_out(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                              min_date=user.check_in + timedelta(days=1), locale='ru').build()
    bot.send_message(chat_id, 'выберите дату выезда', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def call_back1(call: types.CallbackQuery) -> None:
    chat_id = call.message.chat.id
    user = User.user_data[chat_id]

    result, key, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today(), locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text('далее...', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        user.check_in = result
        logger.info(f'{chat_id} написал {result}')

        bot.delete_message(call.message.chat.id, call.message.message_id)
        set_check_out(call.message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def call_back2(call: types.CallbackQuery) -> None:
    chat_id = call.message.chat.id
    user = User.user_data[chat_id]
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 min_date=user.check_in + timedelta(days=1),
                                                 locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text('далее...', call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        user.check_out = result
        logger.info(f'{chat_id} написал {result}')

        bot.delete_message(call.message.chat.id, call.message.message_id)
        if user.current_command == '/bestdeal':
            msg = bot.send_message(chat_id, 'Введите желаемую минимальную стоимость в рублях')
            bot.register_next_step_handler(msg, set_price_min_step)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('1', '3', '5')
            msg = bot.send_message(chat_id, 'Сколько отелей показать?', reply_markup=markup)
            bot.register_next_step_handler(msg, set_number_hotels_step)


def set_price_min_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'Введите стоимость цифрами')
        bot.register_next_step_handler(msg, set_price_min_step)
    else:
        user.price_min = message.text

        msg = bot.send_message(chat_id, 'Введите желаемую максимальную стоимость в рублях')
        bot.register_next_step_handler(msg, set_price_max_step)


def set_price_max_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit() or int(user.price_min) > int(message.text):
        msg = bot.send_message(chat_id, 'Введите стоимость больше указанной минимальной')
        bot.register_next_step_handler(msg, set_price_max_step)
    else:
        user.price_max = message.text
        msg = bot.send_message(chat_id, 'Введите желаемое минимальное расстояние до центра (в километрах)')
        bot.register_next_step_handler(msg, set_min_distance_step)


def set_min_distance_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'Введите расстояние цифрами')
        bot.register_next_step_handler(msg, set_min_distance_step)
    else:
        user.min_distance_from_center = message.text
        msg = bot.send_message(chat_id, 'Введите желаемое максимальное расстояние до центра (в километрах)')
        bot.register_next_step_handler(msg, set_max_distance_step)


def set_max_distance_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit() or int(user.min_distance_from_center) > int(message.text):
        msg = bot.send_message(chat_id, 'Введите расстояние больше указанной минимальной')
        bot.register_next_step_handler(msg, set_max_distance_step)
    else:
        user.max_distance_from_center = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('1', '3', '5')
        msg = bot.send_message(chat_id, 'Сколько отелей показать?', reply_markup=markup)
        bot.register_next_step_handler(msg, set_number_hotels_step)


def set_number_hotels_step(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'Введите количество цифрами или выберите ответ из предложенных')
        bot.register_next_step_handler(msg, set_number_hotels_step)
    else:
        user.hotels_num = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(chat_id, 'Показать фотографии?', reply_markup=markup)
        bot.register_next_step_handler(msg, show_photo)


def show_photo(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if message.text.lower() == 'нет':
        user.photos_num = 0
        bot.send_message(chat_id, 'Уже ищу!')
        send_results(message)

    elif message.text.lower() == 'да':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('1', '3', '5')
        msg = bot.send_message(chat_id, 'Сколько фото показать?', reply_markup=markup)
        bot.register_next_step_handler(msg, set_photo_num)

    else:
        msg = bot.send_message(chat_id, 'Введите Да/Нет или выберите ответ из предложенных')
        bot.register_next_step_handler(msg, show_photo)


def set_photo_num(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]
    logger.info(f'{chat_id} написал {message.text}')

    if not message.text.isdigit():
        msg = bot.send_message(chat_id, 'Введите количество цифрами или выберите ответ из предложенных')
        bot.register_next_step_handler(msg, set_photo_num)
    else:
        user.photos_num = message.text

        bot.send_message(chat_id, 'Уже ищу!')
        send_results(message)


@logger.catch
def send_results(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User.user_data[chat_id]

    if user.current_command == '/bestdeal':
        logger.info('Работает функция для /bestdeal')

        user.hotels = hotels_api.get_bestdeal_hotels(city_id=user.city_id,
                                                     page_size=user.hotels_num,
                                                     check_in=user.check_in,
                                                     check_out=user.check_out,
                                                     price_min=user.price_min,
                                                     price_max=user.price_max,
                                                     min_dist=user.min_distance_from_center,
                                                     max_dist=user.max_distance_from_center)

    elif user.current_command == '/lowprice' or '/highprice':
        logger.info('Работает функция для /lowprice и /highprice')

        user.hotels = hotels_api.get_hotels(city_id=user.city_id,
                                            page_size=user.hotels_num,
                                            check_in=user.check_in,
                                            check_out=user.check_out,
                                            sort=user.sort)
    if user.hotels is None:
        logger.info(f' для {User.user_data[chat_id]} ничего не найдено')
        bot.send_message(chat_id, 'По заданным параметрам не удалось ничего найти')

    if user.hotels:
        for i_key, i_value in user.hotels.items():
            if user.photos_num != 0:
                user.photos = hotels_api.get_photos(i_key, user.photos_num)

            hotel_info = ''
            for j_key, j_value in i_value.items():
                hotel_info += f'{j_key}: {j_value}\n'
            bot.send_message(chat_id, hotel_info, disable_web_page_preview=True)
            user.results += f'{hotel_info}\n'

            if user.photos_num != 0:
                if user.photos is None:
                    bot.send_message(chat_id, 'Фотографии недоступны')
                else:
                    bot.send_media_group(chat_id, user.photos)

        hotels_api.history(user=chat_id, command=user.current_command, result=user.results)
        user.results = ''


def run_bot():
    bot.infinity_polling()

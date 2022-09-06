from loguru import logger
from .welcome import bot
from telebot import types
from users import User


@bot.message_handler(commands=['help'])
def get_help(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User(chat_id)
    User.user_data[chat_id] = user
    logger.info(f'{chat_id} написал {message.text}')

    bot.send_message(
        chat_id,
        'выбери одну из команд:\n/help — помощь по командам бота,\n'
        '/lowprice — вывод самых дешёвых отелей в городе,\n'
        '/highprice — вывод самых дорогих отелей в городе,\n'
        '/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра,\n'
        '/history — вывод истории поиска отелей\n'
    )

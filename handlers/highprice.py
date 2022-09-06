from loguru import logger
from .welcome import bot, set_city_step
from telebot import types
from users import User


@bot.message_handler(commands=['highprice'])
def get_command(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User(chat_id)
    User.user_data[chat_id] = user
    user.sort = 'PRICE_HIGHEST_FIRST'
    user.current_command = '/highprice'

    logger.info(f'{chat_id} написал {message.text}')

    msg = bot.send_message(chat_id, 'В каком городе ищем (кроме городов РФ)?')
    bot.register_next_step_handler(msg, set_city_step)

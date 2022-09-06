from loguru import logger
from .welcome import bot, set_city_step
from telebot import types
from users import User


@bot.message_handler(commands=['lowprice'])
def low_price(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User(chat_id)
    User.user_data[chat_id] = user
    user.current_command = '/lowprice'

    logger.info(f'{chat_id} написал {message.text}')

    msg = bot.send_message(chat_id, 'В каком городе ищем (кроме городов РФ)?')
    bot.register_next_step_handler(msg, set_city_step)


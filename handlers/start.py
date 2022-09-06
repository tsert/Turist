from loguru import logger
from .welcome import bot
from telebot import types
from users import User


@bot.message_handler(commands=['start'])
def start(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User(chat_id)
    User.user_data[chat_id] = user
    logger.info(f'{chat_id} написал {message.text}')
    mess = f'Привет, <b>{message.from_user.last_name} {message.from_user.first_name}.</b> ' \
           f'Чтобы посмотреть список доступных команд набери /help.'
    bot.send_message(chat_id, mess, parse_mode='html')

from loguru import logger
from .welcome import bot
from telebot import types
from users import User


@bot.message_handler(commands=['history'])
def get_history(message: types.Message) -> None:
    chat_id = message.chat.id
    user = User(chat_id)
    User.user_data[chat_id] = user
    logger.info(f'{chat_id} написал {message.text}')

    try:
        with open(f'history/{chat_id}.txt', 'r', encoding='utf-8') as file:
            msg = ''
            for elem in file:
                if '***' in elem:
                    bot.send_message(chat_id, msg, disable_web_page_preview=True)
                    msg = ''
                else:
                    msg += elem
                    if len(msg) > 3800:
                        bot.send_message(chat_id, msg, disable_web_page_preview=True)
                        msg = ''
    except FileNotFoundError:
        bot.send_message(chat_id, 'История пуста')
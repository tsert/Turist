from telebot.types import Message
from .welcome import bot


# Это хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(stat=None)
def bot_echo(message: Message):
    bot.reply_to(message, f"Эхо без состояния или фильтра. \nСообщение: {message.text}")

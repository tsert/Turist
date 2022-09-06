import os
from dotenv import find_dotenv, load_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env\n'
         'Необходимо верно заполнить данные в файле .env.template и переименовать его в .env')
else:
    load_dotenv()


# Уникальный ключ телеграмм бота -> загружается из файла .env
BOT_TOKEN = os.getenv('TOKEN')

# Уникальный ключ  для "hotels4.p.rapidapi.com" -> загружается из файла .env
RAPID_API_KEY = os.getenv('KEY')

# Формат логирования
LOG_FORMAT = '{time:DD-MM-YYYY at HH:mm:ss} | {level: <8} | file: {file: ^30} | func: {function: ^30} | ' \
             'line: {line: >3} | message: {message}'

# Параметр уровня логирования
LOG_LEVEL = 'DEBUG'

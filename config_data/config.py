import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, файл .env отсутствует!")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DB_NAME = os.getenv("DB_NAME")
DEFAULT_COMMANDS = (('start', "Запуск бота"),
                    ('help', 'Получение справочника'),
                    ('day_watch', 'Получение данных торгового дня'),
                    ('equity', 'Получение рыночных данных'),
                    ('symbol_data', 'Получение данных о компании'),
                    ('news', 'Получение новостей с выбором категории'),
                    ('analysis', 'Получение анализа по символу'),
                    )

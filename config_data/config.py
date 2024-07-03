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
                    ('help', 'Вывод команд бота (Справочник)'),
                    ('history', 'Вывод истории запросов'),
                    ('', ''),
                    )

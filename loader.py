from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from config_data import config

bot = Bot(token=config.BOT_TOKEN)  # Объект бота
storage = MemoryStorage()  # Объект сохранения пользовательских состояний
dp = Dispatcher(storage=storage)

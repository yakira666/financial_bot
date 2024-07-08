from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from config_data import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
db = config.DB_NAME

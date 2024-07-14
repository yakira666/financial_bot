from aiogram.filters import Command
from aiogram.types import Message
from loader import main_router
from config_data.config import DEFAULT_COMMANDS



@main_router.message(Command('help'))
async def cmd_help(message: Message):
    text = "\n".join([f'/{k} - {i}' for k, i in DEFAULT_COMMANDS])
    await message.answer(f"Это бот помощник по финансовому рынку! Его команды:\n{text}")

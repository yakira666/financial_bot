from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router
from config_data.config import DEFAULT_COMMANDS

router_1 = Router()


@router_1.message(Command('help'))
async def cmd_help(message: Message):
    text = "\n".join([f'/{k} - {i}' for k, i in DEFAULT_COMMANDS])
    await message.answer(f"Это бот помощник по финансовому рынку! Его команды:\n{text}")

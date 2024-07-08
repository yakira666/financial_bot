from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from config_data.config import DEFAULT_COMMANDS

router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    text = "\n".join([f'/{k} - {i}' for k, i in DEFAULT_COMMANDS])
    await message.answer(f"Это бот помощник по финансовому рынку! Его команды:\n{text}")

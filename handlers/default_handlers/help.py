from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router

router_1 = Router()


@router_1.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f"Команда /help")

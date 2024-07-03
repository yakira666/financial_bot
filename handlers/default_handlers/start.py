from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from loguru import logger
from aiogram import Router

router = Router()

logger.info("Команда start активирована")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет {message.chat.full_name}. Рад тебя видеть!')

from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from aiogram import Router
from database.add_to_db import add_user

router = Router()

logger.info("Команда start активирована")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message)
    await message.answer(f'Привет {message.from_user.full_name}. Рад тебя видеть!')

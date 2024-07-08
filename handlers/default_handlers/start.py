from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from aiogram import Router
from database.add_to_db import add_user
from config_data.config import DEFAULT_COMMANDS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f'Начало работы бота')
    await add_user(message)
    text = "\n".join([f'/{k} - {i}' for k, i in DEFAULT_COMMANDS[2::]])
    await message.answer(f'Привет {message.from_user.full_name}, рад тебя видеть.\nВот что я умею:\n{text}')

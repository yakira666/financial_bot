import datetime

from loader import main_router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import types

from utils.api_request import request, request_for_profile


@main_router.message(Command('symbol_data'))
async def news_func(message: Message):
    logger.info(f'Вывод данных по символу для пользователя {message.chat.id}')

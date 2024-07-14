import datetime

from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import types
from loader import main_router
from utils.api_request import request, request_for_profile


@main_router.message(Command('news'))
async def news_func(message: Message):
    logger.info(f'Вывод новостей по символу для пользователя {message.chat.id}')

from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards


@main_router.message(Command('news'))
async def news_func(message: Message):
    logger.info(f'Запрос на новости от пользователя с User_id: {message.chat.id}')
    await create_keyboards(message)

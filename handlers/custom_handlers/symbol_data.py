from loader import main_router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from keyboards.reply.symbol_menu import cmd_create_menu


@main_router.message(Command('symbol_data'))
async def news_func(message: Message):
    logger.info(f'Вывод данных по символу для пользователя {message.chat.id}')
    await cmd_create_menu(message)

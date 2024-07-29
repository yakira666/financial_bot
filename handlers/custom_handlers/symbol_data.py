import datetime
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from loader import main_router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import types
from keyboards.reply.symbol_menu import cmd_crate_menu

from utils.api_request import request, request_for_profile


@main_router.message(Command('symbol_data'))
async def news_func(message: Message, state: FSMContext):
    logger.info(f'Вывод данных по символу для пользователя {message.chat.id}')
    await cmd_crate_menu(message)

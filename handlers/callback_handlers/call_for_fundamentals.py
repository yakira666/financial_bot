from loader import main_router
from aiogram import types
from loguru import logger
from aiogram.types import Message
from keyboards.inline.keyboard_for_fundamentals import category_fund
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request
from database.add_to_db import add_query_news
from keyboards.reply import news_answer_for_while
import traceback
from datetime import datetime


@main_router.callback_query(lambda callback_value: callback_value.data in category_fund)
async def top_gainers(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Пришел callback из keyboard_for_fundamentals")
    await state.set_state(UserState.fundamentals_ticker_state)
    await state.update_data(category_fundamentals=callback.data[:-12:])
    await callback.message.answer(
        f"Фундаментальные сведения по категории: <b>{callback.data[:-12:]}</b>\n\nВведите тикер или имя компании ...")

from loader import main_router
from aiogram import types
from loguru import logger
from aiogram.types import Message
from keyboards.inline.keyboard_for_news import category
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request, request_for_profile
from database.add_to_db import add_query_news
import traceback


temp_data = {}


@main_router.callback_query(lambda callback_value: callback_value.data in category)
async def top_gainers(callback: types.CallbackQuery, state: FSMContext):
    global temp_data
    logger.info("Пришел callback")
    if callback.data == "market-news::ticker":
        print("TYT TICKER")
    else:
        await state.set_state(UserState.var_news_state)
        async with state.proxy() as data:
            data['category_news'] = callback.data
        await callback.message.answer(f"Ваша категория новостей: <b>{callback.data[13::]}</b>"
                                      f"\n\nКакое <b>количество</b> новостей вы хотите получить (максимум 40)? ")


@main_router.message(UserState.var_news_state)
async def func(message: Message, state: FSMContext):
    global temp_data
    try:
        if int(message.text) <= 40:
            async with state.proxy() as data:

                result_res = request("GET", "https://seeking-alpha.p.rapidapi.com/news/v2/list",
                                 querystring={'size': int(message.text),
                                              'category': data['category_news']})
            for k in result_res.json()['data']:
                url = f"{k['links']['canonical']}"
                text = f"[{k['attributes']['title']}]({url})"
                await message.answer(text, parse_mode="Markdown")
            logger.info(f"Выданы новости пользователю c User_id:{message.chat.id}")
            # await state.set_state(UserState.news_state)
            await message.answer('Если интересует другая новость введите ... ')
    except:
        logger.info(f'Введена неправильная команда!\n{traceback.format_exc()}')
        await message.answer('Вы ввели неправильно число!')  # Доделать более подробно
        return



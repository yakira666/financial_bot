from loader import main_router
from aiogram import types
from loguru import logger
from aiogram.types import Message
from keyboards.inline.keyboard_for_news import category
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request
from database.add_to_db import add_query_news
from keyboards.reply import news_answer_for_while
import traceback
from datetime import datetime


@main_router.callback_query(lambda callback_value: callback_value.data in category)
async def top_gainers(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Пришел callback")
    if callback.data == "market-news::ticker":
        await callback.message.answer("Введите имя компании или ее тикер!")
        await state.set_state(UserState.ticker_news_state)
    else:
        await state.set_state(UserState.var_news_state)
        await state.update_data(category_news=callback.data)
        await callback.message.answer(f"Ваша категория новостей: <b>{callback.data[13::]}</b>"
                                      f"\n\nКакое <b>количество</b> новостей вы хотите получить (максимум 40)? ")


@main_router.message(UserState.var_news_state)
async def func(message: Message, state: FSMContext):
    temp_link_dict = {}
    count = 1
    try:
        if int(message.text) <= 40:
            data = await state.get_data()
            category_news = data.get('category_news')
            result_res = request("GET", "https://seeking-alpha.p.rapidapi.com/news/v2/list",
                                 querystring={'size': int(message.text),
                                              'category': category_news})

            for k in result_res.json()['data']:
                url = f"{k['links']['canonical']}"
                text = f"[{k['attributes']['title']}]({url})"
                temp_link_dict[count] = url
                count += 1
                await message.answer(text, parse_mode="Markdown")
            logger.info(f"Выданы новости пользователю c User_id:{message.chat.id}")
            await add_query_news(
                {"user_id": message.chat.id, "category_news": category_news, "quantity_news": len(temp_link_dict),
                 "link_list": str(temp_link_dict), "date": datetime.now()})
            await news_answer_for_while.cmd_start(message)
            await state.clear()
    except:
        logger.info(f'Введена неправильная команда!\n{traceback.format_exc()}')
        await message.answer('Вы ввели неправильно число!')  # Доделать более подробно
        return

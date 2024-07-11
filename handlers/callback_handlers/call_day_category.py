import datetime

from aiogram import F, Router
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import types

from utils.api_request import request, request_for_profile

router = Router()

values_list = ["top_gainers", "top_losers", "cryptocurrencies", "most_active", "in_the_news", "faang_stocks",
               "sp500_gainers", "sp500_losers", "cap400_gainers", "cap400_losers", "cap600_gainers", "cap600_losers"]


@router.callback_query(lambda F: F.data in values_list)
async def top_gainers(callback: types.CallbackQuery):
    try:
        res = request('GET', "https://seeking-alpha.p.rapidapi.com/market/get-day-watch", {})
        logger.info(f'Отправка запроса get_day_watch на сервер. Статус запроса: {res.status_code}')
        respone_res = res.json()['data']['attributes'][callback.data]
        result_return = f'<b>{callback.data.upper()}:</b>\n'
        for atr in respone_res:
            res_2 = request_for_profile('GET', {"symbols": atr['slug']})
            result_return += f"{atr['slug']} - {atr['name']}, " \
                             f"price from {res_2.json()['data'][0]['attributes']['lastDaily']['rtTime'][:10]}: <b>{res_2.json()['data'][0]['attributes']['lastDaily']['last']}</b>\n"
        await callback.message.answer(result_return)
    except (KeyError, TypeError):
        logger.info(f'Ошибка типа или ключа при запросе на get-day-watch. Возможно недоступен сервер')

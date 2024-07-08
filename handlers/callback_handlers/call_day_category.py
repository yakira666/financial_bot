from aiogram import F, Router
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import types

from utils.api_request import request

router = Router()

values_list = ["top_gainers", "top_losers", "cryptocurrencies", "most_active", "in_the_news", "faang_stocks",
               "sp500_gainers", "sp500_losers", "cap400_gainers", "cap400_losers", "cap600_gainers", "cap600_losers"]


@router.callback_query(lambda F: F.data in values_list)
async def top_gainers(callback: types.CallbackQuery):
    res = request('GET', "https://seeking-alpha.p.rapidapi.com/market/get-day-watch", {})
    respone_res = res.json()['data']['attributes'][callback.data]
    result_return = f'{(callback.data).upper()}:\n'
    for atr in respone_res:
        result_return += f"{atr['slug']} - {atr['name']}\n"
    await callback.message.answer(result_return)

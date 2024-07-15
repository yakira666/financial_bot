from loguru import logger
from aiogram import types
from loader import main_router
from utils.api_request import request, request_for_profile

values_list = ["top_gainers", "top_losers", "cryptocurrencies", "most_active", "in_the_news", "faang_stocks",
               "sp500_gainers", "sp500_losers", "cap400_gainers", "cap400_losers", "cap600_gainers", "cap600_losers"]


# Не нравится как долго работает функция, возможно нужно будет просто делать запрос на стороне
# по с задежкой предположим 2 минуты и пересохранять в бд, а из бд уже дергать в функции и выводить юзеру

@main_router.callback_query(lambda callback_value: callback_value.data in values_list)
async def top_gainers(callback: types.CallbackQuery):
    res = request('GET', "https://seeking-alpha.p.rapidapi.com/market/get-day-watch", {})
    logger.info(f'Отправка запроса {callback.data} на сервер. Статус запроса: {res.status_code}')
    response_res = res.json()['data']['attributes'][callback.data]
    result_return = f'<b>{callback.data.upper()}:</b>\n'
    for atr in response_res:
        res_2 = request_for_profile('GET', {"symbols": atr['slug']})
        result_return += f"{atr['slug']} - {atr['name']}, " \
                         f"price <b>{res_2.json()['data'][0]['attributes']['lastDaily']['last']}</b> from {res_2.json()['data'][0]['attributes']['lastDaily']['rtTime'][:10]}\n"
    await callback.message.answer(f"{result_return}")

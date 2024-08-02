import traceback
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from keyboards.reply import news_answer_for_while
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards_category
from keyboards.inline.keyboard_for_news import create_keyboards_for_symbol_for_news
from keyboards.inline.keyboard_for_fundamentals import create_keyboards_fundamentals,create_keyboards_for_symbol_for_fundamentals
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request, auto_complete_func


@main_router.message(UserState.fundamentals_ticker_state)
async def find_news_for_ticker(message: Message, state: FSMContext):
    res_req = await auto_complete_func(message)
    if res := res_req.json()['symbols']:
        for k in res:
            if k['slug'] == message.text.lower():
                logger.info(f"Найден тикер для фундаментальных сведеней {k['slug']} отправка User_id:{message.chat.id}")
                await message.answer(f"Мы нашли ваш тикер: <b>{k['name'].replace('</b>', '').replace('<b>', '')}</b>")
                data_fund = await state.get_data()
                res_category_fundamentals = data_fund.get('category_fundamentals')
                querystring_quarterly = {"symbol": f"{k['slug']}", "limit": "4", "period_type": "quarterly",
                                         "field": f"{res_category_fundamentals}"}
                querystring_annual = {"symbol": f"{k['slug']}", "limit": "4", "period_type": "annual",
                                      "field": f"{res_category_fundamentals}"}
                request_result_for_fund_in_quarterly = request("GET",
                                                               'https://seeking-alpha.p.rapidapi.com/symbols/get-fundamentals',
                                                               querystring=querystring_quarterly)
                request_result_for_fund_in_annual = request("GET",
                                                            'https://seeking-alpha.p.rapidapi.com/symbols/get-fundamentals',
                                                            querystring=querystring_annual)
                print(request_result_for_fund_in_quarterly.text)
                print(request_result_for_fund_in_annual.json())
                return
            else:
                await create_keyboards_for_symbol_for_fundamentals(message, res_req, 'fundamentals')
                return

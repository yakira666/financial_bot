from loader import main_router
from aiogram import types
from loguru import logger
from aiogram.types import Message
from keyboards.inline.keyboard_for_fundamentals import category_fund
from keyboards.inline.keyboard_for_fundamentals import fundaments_dict
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request
from database.add_to_db import add_query_news
from keyboards.reply import news_answer_for_while
import traceback
from datetime import datetime

from utils.custom_format_func import custom_format


@main_router.callback_query(lambda callback_value: callback_value.data in category_fund)
async def top_gainers(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Пришел callback из keyboard_for_fundamentals поймали категорию")
    await state.set_state(UserState.fundamentals_ticker_state)
    await state.update_data(category_fundamentals=callback.data[:-12:])
    await callback.message.answer(
        f"Фундаментальные сведения по категории: <b>{callback.data[:-12:]}</b>\n\nВведите тикер или имя компании ...")


@main_router.callback_query(lambda callback_value: callback_value.data in fundaments_dict[f"{callback_value.message.chat.id}"])
async def fundamentals_call_slug(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Пришел callback из keyboard_for_fundamentals поймали тикер")
    try:
        data_fund = await state.get_data()
        res_category_fundamentals = data_fund.get('category_fundamentals')
        querystring_quarterly = {"symbol": f"{callback.data[:-12:]}", "limit": "4", "period_type": "quarterly",
                                 "field": f"{res_category_fundamentals}"}
        querystring_annual = {"symbol": f"{callback.data[:-12:]}", "limit": "4", "period_type": "annual",
                              "field": f"{res_category_fundamentals}"}
        request_result_for_fund_in_quarterly = request("GET",
                                                       'https://seeking-alpha.p.rapidapi.com/symbols/get-fundamentals',
                                                       querystring=querystring_quarterly)
        request_result_for_fund_in_annual = request("GET",
                                                    'https://seeking-alpha.p.rapidapi.com/symbols/get-fundamentals',
                                                    querystring=querystring_annual)
        res_answer_quarterly = f"{res_category_fundamentals} in quarterly:\n"
        res_answer_annual = f"{res_category_fundamentals} in annual:\n"
        for r in request_result_for_fund_in_quarterly.json()['data']:
            res_answer_quarterly += f'from period_end_date {(r["attributes"]["period_end_date"]).split("T")[0]} - <b>{custom_format(r["attributes"]["value"])}</b>\n'
        for r in request_result_for_fund_in_annual.json()['data']:
            res_answer_annual += f'from period_end_date {(r["attributes"]["period_end_date"]).split("T")[0]} - <b>{custom_format(r["attributes"]["value"])}</b>\n'
        await callback.message.answer(f"{res_answer_quarterly}\n{res_answer_annual}")
        return
    except:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {traceback.format_exc()}")

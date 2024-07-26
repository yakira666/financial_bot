from aiogram import types, F
from loader import main_router
from aiogram.fsm.context import FSMContext
from database.add_to_db import add_query
from states.user_states import UserState

values_list = []
values_list_news = []


@main_router.callback_query(lambda callback_value: callback_value.data in values_list)
async def call_for_analysis(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.analysis_state)
    await add_query({'chat_id': callback.message.chat.id, "data_symbol": callback.data})
    await callback.message.answer("Сколько вы бы хотели видеть аналитических статей? (максимальное кол-во 40).")
    return callback.data


@main_router.callback_query(F.data == 'back_to_symbol')
async def call_for_back(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.symbol_for_analysis_state)
    await callback.message.answer('Пожалуйста введите новый тикер для вывода аналитических статей!')


@main_router.callback_query(lambda callback_value: callback_value.data in values_list_news)
async def call_for_analysis(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Сколько вы бы хотели видеть новостных статей? (максимальное кол-во 40).")
    await state.set_state(UserState.var_news_state)
    return callback.data


@main_router.callback_query(F.data == 'back_to_symbol' + 'news')
async def call_for_back(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.ticker_news_state)
    await callback.message.answer('Пожалуйста введите новый тикер для вывода новостей!')

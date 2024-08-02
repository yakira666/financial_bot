from aiogram import F
from aiogram import types

from keyboards.inline.keyboard_for_fundamentals import create_keyboards_fundamentals
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards_category
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
from utils.api_request import request


async def cmd_create_menu(message: types.Message):
    # ГОТОВО
    kb = [
        [
            types.KeyboardButton(text="Получить оценку"),
            types.KeyboardButton(text="Получить диаграмму"),
            types.KeyboardButton(text="Получить фундаментные сведения")
        ],
        [
            types.KeyboardButton(text="Получить новости"),
            types.KeyboardButton(text="Получить анализ"),
            types.KeyboardButton(text="Вернуться в основное меню"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
    await message.answer("Что вас интересует?", reply_markup=keyboard)


@main_router.message(F.text.lower() == "получить оценку")
# ГОТОВО
async def symbol_news(message: types.Message, state: FSMContext):
    await message.answer("Введите тикер или имя компании...", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.valuation)


@main_router.message(F.text.lower() == "получить диаграмму")
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите диаграмму", reply_markup=types.ReplyKeyboardRemove())

    # Запрос данных (исправьте URL и параметры запроса, если необходимо)
    res_req = request("GET", "https://seeking-alpha.p.rapidapi.com/symbols/get-chart",
                      querystring={'symbol': 'aapl', 'period': '1D'})


@main_router.message(F.text.lower() == "получить фундаментные сведения")
async def symbol_news(message: types.Message):
    await message.answer("Выберите категорию которая вам интересна, и подождите какое-то время:", reply_markup=types.ReplyKeyboardRemove())
    await create_keyboards_fundamentals(message)

@main_router.message(F.text.lower() == "получить новости")
# ГОТОВО
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите", reply_markup=types.ReplyKeyboardRemove())
    await create_keyboards_category(message)


@main_router.message(F.text.lower() == "получить анализ")
# ГОТОВО
async def symbol_analysis(message: types.Message, state: FSMContext):
    await message.answer("Введите имя компании или ее тикер!", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.symbol_for_analysis_state)


@main_router.message(F.text.lower() == "вернуться в основное меню")
# ГОТОВО
async def no(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите другую команду...", reply_markup=types.ReplyKeyboardRemove())

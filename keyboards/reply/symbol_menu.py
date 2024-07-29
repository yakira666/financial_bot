from aiogram import F
from aiogram import types
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards_category
from aiogram.fsm.context import FSMContext
import time
from states.user_states import UserState


async def cmd_create_menu(message: types.Message):
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
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите оценку", reply_markup=types.ReplyKeyboardRemove())


@main_router.message(F.text.lower() == "получить диаграмму")
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите диаграмму", reply_markup=types.ReplyKeyboardRemove())


@main_router.message(F.text.lower() == "получить фундаментные сведения")
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите фундаментные сведения", reply_markup=types.ReplyKeyboardRemove())


@main_router.message(F.text.lower() == "получить новости")
async def symbol_news(message: types.Message):
    await message.answer("ok... подождите", reply_markup=types.ReplyKeyboardRemove())
    await create_keyboards_category(message)


@main_router.message(F.text.lower() == "получить анализ")
async def symbol_analysis(message: types.Message, state: FSMContext):
    await message.answer("Введите символ по которому хотите получить анализ!", reply_markup=types.ReplyKeyboardRemove())
    # await news_func(message, state)


@main_router.message(F.text.lower() == "вернуться в основное меню")
async def no(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите другую команду...", reply_markup=types.ReplyKeyboardRemove())

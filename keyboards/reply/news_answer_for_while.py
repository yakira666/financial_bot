from aiogram import F
from aiogram import types
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards_category
from aiogram.fsm.context import FSMContext
import time


async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
    await message.answer("Вас интересуют еще новости?", reply_markup=keyboard)


@main_router.message(F.text.lower() == "да")
async def yes(message: types.Message):
    await message.answer("ok... подождите", reply_markup=types.ReplyKeyboardRemove())
    time.sleep(1)
    await create_keyboards_category(message)


@main_router.message(F.text.lower() == "нет")
async def no(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите другую команду...", reply_markup=types.ReplyKeyboardRemove())

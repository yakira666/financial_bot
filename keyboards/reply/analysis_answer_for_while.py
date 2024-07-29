from aiogram import F
from aiogram import types
from loader import main_router
from aiogram.fsm.context import FSMContext
from states.user_states import UserState


async def cmd_start_analysis(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да, продолжить аналитику!"),
            types.KeyboardButton(text="Нет, остановить аналитику!")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
    await message.answer("Хотите продолжить получить аналитику?", reply_markup=keyboard)


@main_router.message(F.text.lower() == "да, продолжить аналитику!")
async def yes(message: types.Message, state: FSMContext):
    await message.answer("ОК... введите другой тикер!", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.symbol_for_analysis_state)


@main_router.message(F.text.lower() == "нет, остановить аналитику!")
async def no(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите другую команду...", reply_markup=types.ReplyKeyboardRemove())

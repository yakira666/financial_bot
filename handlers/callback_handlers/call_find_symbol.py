from aiogram import types
from loader import main_router
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
from database.add_to_db import add_query


values_list = []


@main_router.callback_query(lambda callback_value: callback_value.data in values_list)
async def call_for_analysis(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.analysis)
    await add_query({'chat_id': callback.message.chat.id, "data_symbol": callback.data})
    await callback.message.answer("Сколько вы бы хотели видеть аналитических статей? (максимальное кол-во 40).")
    return callback.data

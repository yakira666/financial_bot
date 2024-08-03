from aiogram.filters import Command
from aiogram.types import Message
from loader import main_router
from config_data.config import DEFAULT_COMMANDS
from aiogram.fsm.context import FSMContext


@main_router.message(Command('cancel'))
async def cmd_help(message: Message, state: FSMContext):
    text = "\n".join([f'/{k} - {i}' for k, i in DEFAULT_COMMANDS[2::]])
    await state.clear()
    await message.answer(f"Состояние сброшено, можно выбрать одну из команд:\n{text}")

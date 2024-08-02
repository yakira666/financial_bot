import traceback
from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger


async def cmd_start_decryption(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    try:
        keyboard.add(InlineKeyboardButton(text="Да, получить!", callback_data="Да, получить!"))
        keyboard.add(InlineKeyboardButton(text="Нет, отказаться!", callback_data="Нет, отказаться!"))
        keyboard.adjust(2)
        await message.answer('<b>Получить пояснения на русском?</b>:',
                             reply_markup=keyboard.as_markup(resize_keyboard=True))
    except:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры: {traceback.format_exc()}")
    return keyboard

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback


async def create_keyboards(message, res):
    keyboard = InlineKeyboardBuilder()
    result_req = res.json()['data']['attributes']
    try:
        for name_attr in result_req:
            keyboard.add(InlineKeyboardButton(text=name_attr, callback_data=name_attr))
        keyboard.adjust(2)
        await message.answer("Выберите категорию которая вам интересна, и подождите какое-то время:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))
    except KeyError:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {res.status_code}\n{traceback.format_exc()}")
    return keyboard

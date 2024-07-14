from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback
from handlers.callback_handlers.call_find_symbol import values_list


async def create_keyboards(message, res):
    keyboard = InlineKeyboardBuilder()
    try:
        for name_attr in res.json()['symbols']:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{name_attr['name'].replace('</b>', '').replace('<b>', '')}-{name_attr['content'].replace('</b>', '').replace('<b>', '')}",
                    callback_data=name_attr['name'].replace('</b>', '').replace('<b>', '')))
            values_list.append(name_attr['name'].replace('</b>', '').replace('<b>', ''))
        keyboard.adjust(2)
        await message.answer("Вот что нам удалось найти по вашему запросу:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))
    except KeyError:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {res.status_code}\n{traceback.format_exc()}")
    return keyboard

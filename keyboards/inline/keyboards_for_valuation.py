from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback

valuation_list = []


async def create_keyboards(message, res, string):
    keyboard = InlineKeyboardBuilder()
    try:
        symbols = res.json().get('symbols', [])
        logger.debug(f"Creating keyboards for symbols: {symbols}")
        for name_attr in symbols:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{name_attr['name'].replace('</b>', '').replace('<b>', '')}-{name_attr['content'].replace('</b>', '').replace('<b>', '')}",
                    callback_data=(name_attr['name'].replace('</b>', '').replace('<b>', '')) + f' {string}'))
            valuation_list.append(name_attr['name'].replace('</b>', '').replace('<b>', '') + f' {string}')
        keyboard.adjust(2)
        keyboard.row(
            InlineKeyboardButton(text='Назад (выбрать другой тикер)', callback_data=('back_to_symbol' + f'{string}')))
        await message.answer("Вот что нам удалось найти по вашему запросу:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))
    except KeyError as e:
        logger.error(f"KeyError in create_keyboards: {e}")
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"Unexpected error in create_keyboards: {e}")
        logger.error(traceback.format_exc())
    return keyboard

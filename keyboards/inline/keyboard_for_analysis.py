from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback
from handlers.callback_handlers.call_find_symbol import values_list, values_list_news


async def create_keyboards_for_symbol_for_news(message, res):
    keyboard = InlineKeyboardBuilder()
    try:

        for name_attr in res.json()['symbols']:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{name_attr['name'].replace('</b>', '').replace('<b>', '')}-{name_attr['content'].replace('</b>', '').replace('<b>', '')}",
                    callback_data=(name_attr['name'].replace('</b>', '').replace('<b>', '')) + 'news'))
            values_list_news.append(name_attr['name'].replace('</b>', '').replace('<b>', '') + 'news')
        keyboard.adjust(2)
        keyboard.row(
            InlineKeyboardButton(text='Назад (выбрать другой тикер)', callback_data=('back_to_symbol' + 'news')))
        await message.answer("Вот что нам удалось найти по вашему запросу:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))

    except KeyError:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {res.status_code}\n{traceback.format_exc()}")
    return keyboard


async def create_keyboards_for_symbol(message, res):
    keyboard = InlineKeyboardBuilder()
    try:

        for name_attr in res.json()['symbols']:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{name_attr['name'].replace('</b>', '').replace('<b>', '')}-{name_attr['content'].replace('</b>', '').replace('<b>', '')}",
                    callback_data=name_attr['name'].replace('</b>', '').replace('<b>', '')))
            values_list.append(name_attr['name'].replace('</b>', '').replace('<b>', ''))
        keyboard.adjust(2)
        keyboard.row(InlineKeyboardButton(text='Назад (выбрать другой тикер)', callback_data='back_to_symbol'))
        await message.answer("Вот что нам удалось найти по вашему запросу:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))

    except KeyError:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {res.status_code}\n{traceback.format_exc()}")
    return keyboard

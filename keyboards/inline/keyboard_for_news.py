from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback
from aiogram.types import Message

category = ('market-news::ticker|'
            'market-news::all|'
            'market-news::top-news|'
            'market-news::on-the-move|'
            'market-news::market-pulse|'
            'market-news::notable-calls|'
            'market-news::buybacks|'
            'market-news::commodities|'
            'market-news::crypto|'
            'market-news::issuance|'
            'market-news::dividend-stocks|'
            'market-news::dividend-funds|'
            'market-news::earnings|'
            'earnings::earnings-news|'
            'market-news::global|'
            'market-news::guidance|'
            'market-news::ipos|'
            'market-news::spacs|'
            'market-news::politics|'
            'market-news::m-a|'
            'market-news::us-economy|'
            'market-news::consumer|'
            'market-news::energy|'
            'market-news::financials|'
            'market-news::healthcare|'
            'market-news::mlps|'
            'market-news::reits|'
            'market-news::technology').split('|')


async def create_keyboards_category(message: Message):
    keyboard = InlineKeyboardBuilder()
    try:
        for name_c in category:
            keyboard.add(InlineKeyboardButton(text=name_c[13::].strip(), callback_data=name_c))
        keyboard.adjust(4)
        await message.answer("Выберите категорию которая вам интересна, и подождите какое-то время:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))
    except:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры: {traceback.format_exc()}")
    return keyboard

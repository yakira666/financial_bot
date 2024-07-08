from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def create_keyboards(message, res):
    keyboard = InlineKeyboardBuilder()
    for name_attr in res.json()['data']['attributes']:
        keyboard.add(InlineKeyboardButton(text=name_attr, callback_data=name_attr))
    keyboard.adjust(2)
    await message.answer("Выберите категорию которая вам интересна:\n",
                         reply_markup=keyboard.as_markup(resize_keyboard=True))
    return keyboard

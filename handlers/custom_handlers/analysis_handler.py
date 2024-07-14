from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from database.add_to_db import add_query
from states.user_states import UserState
from utils.api_request import request
from keyboards.inline.keyboard_for_analysis import create_keyboards
from loader import main_router
from database.read_from_db import read_query


@main_router.message(Command('analysis'))
async def news_func(message: Message, state: FSMContext):
    logger.info(f'Вывод анализа по символу для пользователя {message.chat.id}')
    await message.answer("Введите имя компании или ее тикер")
    await state.set_state(UserState.symbol_for_analysis)


@main_router.message(UserState.symbol_for_analysis)
async def input_symbol(message: Message, state: FSMContext):
    res_req = request("GET", "https://seeking-alpha.p.rapidapi.com/v2/auto-complete",
                      querystring={"query": message.text, 'type': 'symbols', 'size': 10})
    if res := res_req.json()['symbols']:
        for k in res:
            if k['slug'] == message.text.lower():
                logger.info("Все вверно введено выдаем информацию")
                await message.answer(f"Мы нашли ваш тикер: <b>{k['name'].replace('</b>', '').replace('<b>', '')}</b>")
                await state.set_state(UserState.analysis)
                await add_query(
                    {'chat_id': message.chat.id, "data_symbol": k['name'].replace('</b>', '').replace('<b>', '')})
                await message.answer("Сколько вы бы хотели видеть аналитических статей? (максимальное кол-во 40).")
                return
            else:
                await create_keyboards(message, res_req)
                return


@main_router.message(UserState.analysis)
async def analysis_func(message: Message):
    if int(message.text) <= 40:
        print(message.text)
        data = await read_query(message.chat.id)
        unpacked_data = ''.join([item for (item,) in data])
        print(unpacked_data)
        result_res = request("GET", "https://seeking-alpha.p.rapidapi.com/analysis/v2/list",
                             querystring={'id': unpacked_data, 'size': int(message.text)})
        for k in result_res.json()['data']:
            url = f"https://seekingalpha.com/{k['links']['self']}"
            text = f"[{k['attributes']['title']}]({url})"
            await message.answer(text, parse_mode="Markdown")

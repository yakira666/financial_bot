from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from database.add_to_db import add_query
from states.user_states import UserState
from utils.api_request import request
from keyboards.inline.keyboard_for_analysis import create_keyboards_for_symbol
from loader import main_router
from database.read_from_db import read_query
import traceback


@main_router.message(Command('analysis'))
async def news_func(message: Message, state: FSMContext):
    logger.info(f'Запрос символа у пользователя с User_id: {message.chat.id}')
    await message.answer("Введите имя компании или ее тикер!")
    await state.set_state(UserState.symbol_for_analysis_state)


@main_router.message(UserState.symbol_for_analysis_state)
async def input_symbol(message: Message, state: FSMContext):
    res_req = request("GET", "https://seeking-alpha.p.rapidapi.com/v2/auto-complete",
                      querystring={"query": message.text, 'type': 'symbols', 'size': 10})
    if res := res_req.json()['symbols']:
        for k in res:
            if k['slug'] == message.text.lower():
                logger.info(f"Все вверно введено пользователем c User_id:{message.chat.id}, выдаем информацию")
                await message.answer(f"Мы нашли ваш тикер: <b>{k['name'].replace('</b>', '').replace('<b>', '')}</b>")
                await state.set_state(UserState.analysis_state)
                await add_query(
                    {'chat_id': message.chat.id, "data_symbol": k['name'].replace('</b>', '').replace('<b>', '')})
                await message.answer("Сколько вы бы хотели видеть аналитических статей? (максимальное кол-во 40).")
                return
            else:
                await create_keyboards_for_symbol(message, res_req)
                return


@main_router.message(UserState.analysis_state)
async def analysis_func(message: Message, state: FSMContext):
    try:
        if int(message.text) <= 40:
            data = await read_query(message.chat.id)
            unpacked_data = ''.join([item for (item,) in data])
            result_res = request("GET", "https://seeking-alpha.p.rapidapi.com/analysis/v2/list",
                                 querystring={'id': unpacked_data, 'size': int(message.text)})
            for k in result_res.json()['data']:
                url = f"https://seekingalpha.com/{k['links']['self']}"
                text = f"[{k['attributes']['title']}]({url})"
                await message.answer(text, parse_mode="Markdown")
            logger.info(f"Выдан анализ пользователю c User_id:{message.chat.id}")
            await state.set_state(UserState.symbol_for_analysis_state)
            await message.answer('Если интересует другой тикер введите его, или выберете другую команду')

    except:
        logger.info(f'Введена неправильная команда!\n{traceback.format_exc()}')
        await state.set_state(UserState.symbol_for_analysis_state)
        await message.answer(f'Мы не нашли аналитики по этому тикеру, выберете другой тикер, или другую команду!')
        return

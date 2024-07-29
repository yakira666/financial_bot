import traceback
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from keyboards.reply import news_answer_for_while
from loader import main_router
from keyboards.inline.keyboard_for_news import create_keyboards_category
from keyboards.inline.keyboard_for_news import create_keyboards_for_symbol_for_news
from states.user_states import UserState
from aiogram.fsm.context import FSMContext
from utils.api_request import request


@main_router.message(Command('news'))
async def news_func(message: Message):
    logger.info(f'Запрос на новости от пользователя с User_id: {message.chat.id}')
    await create_keyboards_category(message)


@main_router.message(UserState.ticker_news_state)
async def find_news_for_ticker(message: Message, state: FSMContext):
    res_req = request("GET", "https://seeking-alpha.p.rapidapi.com/v2/auto-complete",
                      querystring={"query": message.text, 'type': 'symbols', 'size': 10})
    if res := res_req.json()['symbols']:
        for k in res:
            if k['slug'] == message.text.lower():
                logger.info(f"Все вверно введено пользователем c User_id:{message.chat.id}, выдаем информацию")
                await message.answer(f"Мы нашли ваш тикер: <b>{k['name'].replace('</b>', '').replace('<b>', '')}</b>")
                await state.update_data(news_ticker=message.text.lower())
                await state.set_state(UserState.number_for_ticker_news)
                await message.answer("Сколько вы бы хотели видеть новостных статей? (максимальное кол-во 40).")
                return
            else:
                await create_keyboards_for_symbol_for_news(message, res_req)
                return


@main_router.message(UserState.number_for_ticker_news)
async def analysis_func(message: Message, state: FSMContext):
    try:
        if int(message.text) <= 40:
            data = await state.get_data()
            news_data = data.get('news_ticker')
            result_res = request("GET", "https://seeking-alpha.p.rapidapi.com/news/v2/list-by-symbol",
                                 querystring={'size': int(message.text), 'id': news_data})

            for k in result_res.json()['data']:
                url = f"https://seekingalpha.com/{k['links']['self']}"
                text = f"[{k['attributes']['title']}]({url})"
                await message.answer(text, parse_mode="Markdown")
            logger.info(f"Выданы новости по тикеру, пользователю c User_id:{message.chat.id}")
            await news_answer_for_while.cmd_start(message)
            await state.clear()
        else:
            await message.answer(f'Вы ввели неверное число... Повторите ввод!')
    except:
        logger.info(f'Введена неправильная команда!\n{traceback.format_exc()}')
        await state.set_state(UserState.ticker_news_state)
        await message.answer(f'Мы не нашли новостей по этому тикеру, выберете другой тикер, или другую команду!')
        return

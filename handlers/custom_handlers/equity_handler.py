from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from utils.api_request import request

router = Router()
filterCategory = ("us-equity-markets", "us-equity-sectors", "us-equity-factors", "global-equity", "countries-equity")


@router.message(Command('equity'))
async def equity(message: Message):
    logger.info(f"Вывод данных о рынке")
    for fc in filterCategory:
        res = (request(method='GET', url="https://seeking-alpha.p.rapidapi.com/market/get-equity",
                       querystring={"filterCategory": fc})
               )
        if res.status_code == 200:
            t = res.json()
            res_text = f"\t{fc.upper()}\n"
            for i in t['data']:
                res_text += f"{i['attributes']['name']} - {i['attributes']['company']}, alias_name - {i['attributes']['alias_name']}\n"
            await message.answer(res_text)

import asyncio
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F, Router
from loader import bot
from loguru import logger
from utils.api_request import request
import json

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
            head = message.answer(f"\t{fc.upper()}")
            print(fc.upper())
            print(json.dumps(t['data'], indent=4))
            # for st in t:
            #     await message.answer(st)

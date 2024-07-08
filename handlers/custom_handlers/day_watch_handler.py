from keyboards.inline.keyboard_for_daytime_category import create_keyboards
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from utils.api_request import request

router = Router()


@router.message(Command('day_watch'))
async def day_watch(message: Message):
    logger.info(f"Вывод торгового дня")
    res = request('GET', "https://seeking-alpha.p.rapidapi.com/market/get-day-watch", {})
    await create_keyboards(message, res)

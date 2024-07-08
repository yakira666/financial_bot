from loader import bot, dp, db
from loguru import logger
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

router = Router()


@router.message(Command('day_watch'))
async def day_watch():
    logger.info(f"Вывод торгового дня")
    pass
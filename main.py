from loader import dp, bot
import asyncio
from handlers.default_handlers.start import router
from handlers.default_handlers.help import router_1
from loguru import logger


async def main():
    dp.include_router(router)
    dp.include_router(router_1)
    logger.info(f'Инициализация бота')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
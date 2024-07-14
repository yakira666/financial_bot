from loader import dp, bot, main_router
import asyncio
from handlers import default_handlers, custom_handlers, callback_handlers
from loguru import logger


async def main():
    dp.include_router(main_router)
    logger.info(f'Инициализация бота')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

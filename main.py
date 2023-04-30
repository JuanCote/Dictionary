import os
import logging
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from handlers import add_word, start


async def main():
    API_TOKEN = os.getenv("TELEGRAM_KEY")

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    logging.basicConfig(level=logging.INFO)

    dp.include_routers(start.router, add_word.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

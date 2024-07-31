from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from routers import router as main_router

from dotenv import load_dotenv
import os
import logging
import asyncio


dp = Dispatcher()
dp.include_router(main_router)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    print(BOT_TOKEN)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    asyncio.run(main())

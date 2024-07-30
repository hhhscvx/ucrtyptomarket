from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

from config.config import start_message
from dotenv import load_dotenv
import os
import logging
import asyncio


dp = Dispatcher()


@dp.message(CommandStart)
async def start_message_handler(message: Message):
    await message.answer(start_message)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    asyncio.run(main())

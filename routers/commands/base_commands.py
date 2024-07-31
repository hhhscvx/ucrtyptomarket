from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from config.data import RuTexts
from config.keyboard_start import start_keyboard


router = Router(name=__name__)


@router.message(CommandStart())
async def start_message_handler(message: Message):
    await message.answer(RuTexts.START_MESSAGE, reply_markup=start_keyboard())

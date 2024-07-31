from aiogram import F, Router
from aiogram.types import Message

from config.data import RuTexts
from .profile_keyboard import profile_keyboard


router = Router(name=__name__)


@router.message(F.text == RuTexts.profile)
async def profile_message_handler(message: Message):
    await message.answer(text=message.text,
                         reply_markup=profile_keyboard())

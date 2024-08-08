from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext

from config.data import RuTexts
from config.keyboard_start import start_keyboard
from database import insert


router = Router(name=__name__)


@router.message(CommandStart())
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(RuTexts.START_MESSAGE, reply_markup=start_keyboard())
    user_id = message.from_user.id
    user_username = message.from_user.username
    try:
        insert(table="profiles", column_values={
            "tg_id": user_id,
            "username": user_username,
            "balance": 0.00
        })
    except:
        pass  # user already exist


@router.message(F.text == RuTexts.our_channel)
async def start_message_handler(message: Message):
    await message.answer(RuTexts.OUR_CHANNEL_MESSAGE)


@router.message(F.text == RuTexts.about_us)
async def start_message_handler(message: Message):
    await message.answer(RuTexts.ABOUT_US_MESSAGE)

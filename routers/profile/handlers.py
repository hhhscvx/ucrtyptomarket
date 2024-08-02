from aiogram import F, Router
from aiogram.types import Message

from config.data import RuTexts
from ..profile_keyboard import profile_keyboard
from database import fetchall
from .orders_keyboard import make_orders_history_keyboard


router = Router(name=__name__)


@router.message(F.text == RuTexts.profile)
async def profile_message_handler(message: Message):
    await message.answer(text=message.text,
                         reply_markup=profile_keyboard())


@router.message(F.text == RuTexts.show_balance)
async def profile_message_handler(message: Message):
    balance = fetchall('profiles', ['balance'], f"WHERE tg_id = {message.from_user.id}")
    text = f"Ваш баланс: {balance[0]['balance']}$"
    await message.answer(text=text)


@router.message(F.text == RuTexts.order_history)
async def profile_message_handler(message: Message):
    condition = f"WHERE buyer_tg_id = {message.from_user.id}"
    columns = ['account_type', 'amount', 'created']
    orders = fetchall('orders', columns=columns, condition=condition)
    if not orders:
        await message.answer(text="У вас пока нет заказов...")
    else:
        await message.answer(text="Ваши заказы:", reply_markup=make_orders_history_keyboard(orders))

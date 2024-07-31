from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount


router = Router(name=__name__)


@router.message(BuyAccount.amount, lambda message: message.text.isdigit())
async def handle_buy_account_category(message: Message, state: FSMContext):
    data = await state.update_data(amount=message.text)
    await state.clear()
    from ..handlers import send_order
    await send_order(message, data)


@router.message(BuyAccount.amount)
async def handle_buy_account_category_invalid(message: Message, state: FSMContext):
    await message.answer(f"Это значение недоступно. Пожалуйста, введите количество аккаунтов")

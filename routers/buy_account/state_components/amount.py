from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount
from config.data import get_accounts_count


router = Router(name=__name__)


@router.message(BuyAccount.amount, lambda message: message.text.isdigit())
async def handle_buy_account_category(message: Message, state: FSMContext):
    # ПРОВЕРКА ЧТО СТОЛЬКО АККОВ ВООБЩЕ ЕСТЬ
    data = await state.get_data()
    category = data['category'].lower()
    accounts_count = get_accounts_count(category, "../../config")
    if int(message.text) > accounts_count:
        await message.answer(f"Это значение недоступно. Пожалуйста, введите допустимое число: 1-{accounts_count}")
        return

    data = await state.update_data(amount=message.text)
    await state.set_state(BuyAccount.payment)
    from ..handlers import send_order
    await send_order(message, data)


@router.message(BuyAccount.amount)
async def handle_buy_account_category_invalid(message: Message, state: FSMContext):
    await message.answer(f"Это значение недоступно. Пожалуйста, введите количество аккаунтов")

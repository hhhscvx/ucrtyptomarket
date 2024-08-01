from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount
from ..cb_handlers import _get_accounts_path


router = Router(name=__name__)


@router.message(BuyAccount.amount, lambda message: message.text.isdigit())
async def handle_buy_account_category(message: Message, state: FSMContext):
    # ПРОВЕРКА ЧТО СТОЛЬКО АККОВ ВООБЩЕ ЕСТЬ
    data = await state.get_data()
    path = _get_accounts_path(f"{data['category'].lower()}_accounts.txt", "../../config")
    with open(path, 'r') as file:
        accounts_count = len(list(map(lambda string: string.rstrip('\n'), file.readlines())))
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

import os
from datetime import datetime
import hashlib
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.input_file import FSInputFile

from .keyboards import PaymentConfig, payment_type_keyboard
from config.data import RuTexts
from config.keyboard_start import start_keyboard
from routers.buy_account.states import BuyAccount
from config.data import RuTexts
from database import insert


router = Router(name=__name__)


@router.callback_query(F.data == PaymentConfig.back_to_menu_cb)
async def back_to_menu_cb_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(RuTexts.START_MESSAGE, reply_markup=start_keyboard())


@router.callback_query(F.data == PaymentConfig.payment_cb)
@router.message(BuyAccount.pay_or_leave)
async def success_payment_cb_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    price = RuTexts.twitter_account_price if data['category'] == RuTexts.twitter else RuTexts.discord_account_price
    total = price * float(data['amount'])
    # account_category, amount_accounts = await _answer_and_get_data(callback, state)
    # match(account_category):
    #     case RuTexts.discord:
    #         await send_accounts_and_delete_sold(acc_type=RuTexts.discord, callback=callback, amount_accounts=amount_accounts)
    #     case RuTexts.twitter:
    #         await send_accounts_and_delete_sold(acc_type=RuTexts.twitter, callback=callback, amount_accounts=amount_accounts)
    await callback.message.answer("Выберите тип оплаты", reply_markup=await payment_type_keyboard(total_sum=total))
    await state.clear()


async def _answer_and_get_data(callback: CallbackQuery, state: FSMContext) -> list:
    await callback.answer()
    data = await state.get_data()
    account_category = data['category']
    amount_accounts = int(data['amount'])
    return (account_category, amount_accounts)


def _get_accounts_path(filename: str, location: str) -> str:
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, location)
    accounts_file_path = os.path.join(config_dir, filename)
    return accounts_file_path


def _get_accounts(count: int, accounts: list) -> str:
    res = ''
    for i in range(count):
        res += f"{accounts[i]}\n"
    return res


def _generate_unique_id(accounts_type: str) -> str:
    created = datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S")
    hash_obj = hashlib.md5(f'{accounts_type} {created}'.encode())
    return hash_obj.hexdigest()


def _save_order_to_db(callback: CallbackQuery, account_type: str, amount_accounts: int, accounts: str):
    buyer_tg_id = callback.message.chat.id
    if account_type == 'discord':
        total_sum = RuTexts.discord_account_price * amount_accounts
    elif account_type == 'twitter':
        total_sum = RuTexts.twitter_account_price * amount_accounts
    insert(table="orders", column_values={
        "buyer_tg_id": buyer_tg_id,
        "account_type": account_type,
        "amount": amount_accounts,
        "accounts": accounts,
        "total_sum": total_sum,
        "uuid": _generate_unique_id(account_type)
    })


async def _send_accounts(callback: CallbackQuery, accounts: list, amount_accounts: int) -> None:
    # if amount_accounts == 1:
    #     await callback.message.answer(f"Ваш аккаунт готов!\n\nФормат: почта:пароль:токен"
    #                                   f"\n\n<code>{accounts[0]}</code>")
    # else:
    #     try:
    #         await callback.message.answer(f"Ваши аккаунты готовы!\n\nФормат: почта:пароль:токен\n\n"
    #                                       f"<code>{_get_accounts(amount_accounts, accounts)}</code>")
    #     except TelegramBadRequest as error:
    #         print(f"Some error: {error}")
    file_path = f"accounts_{callback.message.chat.id}"
    with open(file_path, "w") as file:
        file.writelines(_get_accounts(amount_accounts, accounts))
    await callback.message.answer_document(FSInputFile(file_path),
                                           caption="Ваши аккаунты готовы!\n\nФормат: почта:пароль:токен")
    os.remove(file_path)


async def send_accounts_and_delete_sold(acc_type: str, callback: CallbackQuery, amount_accounts: int):
    match(acc_type):
        case RuTexts.discord:
            await send_accounts(callback=callback, account_type='discord', amount_accounts=amount_accounts)
        case RuTexts.twitter:
            await send_accounts(callback=callback, account_type='twitter', amount_accounts=amount_accounts)


async def send_accounts(callback: CallbackQuery, account_type: str, amount_accounts):
    file_path = _get_accounts_path(f'{account_type}_accounts.txt', '../../config')
    with open(file_path, 'r') as file:
        accounts = list(map(lambda string: string.rstrip('\n'), file.readlines()))
        await _send_accounts(callback=callback, accounts=accounts, amount_accounts=amount_accounts)
        _save_order_to_db(callback, account_type, amount_accounts, accounts="\n".join(accounts[:amount_accounts]))
    with open(file_path, 'w') as file:
        file.writelines(
            map(lambda string: f"{string}\n" if not accounts[-1] == string else string, accounts[amount_accounts:]))

import os
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiocryptopay import AioCryptoPay, Networks

from .cb_handlers import (_answer_and_get_data,
                          send_accounts_and_delete_sold)
from config.data import RuTexts
from dotenv import load_dotenv


router = Router(name=__name__)


@router.callback_query(F.data.startswith("invoice_id="))
async def back_to_menu_cb_handler(callback: CallbackQuery, state: FSMContext):
    invoice_id = callback.data.split("=")[1]
    load_dotenv()
    PAY_TOKEN = os.getenv("CRYPTO_TOKEN")
    crypto = AioCryptoPay(PAY_TOKEN, Networks.MAIN_NET)
    invoice = (await crypto.get_invoices(invoice_ids=invoice_id))[0]

    if invoice.status != "paid":
        await callback.answer("Оплата не поступила...")
    else:
        await callback.answer()
        data = await state.get_data()
        price = RuTexts.twitter_account_price if data['category'] == RuTexts.twitter else RuTexts.discord_account_price
        total = price * float(data['amount'])
        account_category, amount_accounts = await _answer_and_get_data(callback, state)
        match(account_category):
            case RuTexts.discord:
                await send_accounts_and_delete_sold(acc_type=RuTexts.discord, callback=callback, amount_accounts=amount_accounts)
            case RuTexts.twitter:
                await send_accounts_and_delete_sold(acc_type=RuTexts.twitter, callback=callback, amount_accounts=amount_accounts)
        await state.clear()

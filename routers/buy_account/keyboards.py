import os
from dotenv import load_dotenv
from aiocryptopay import AioCryptoPay, Networks

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
# from .tinkoff import create_pay_link, check_order_payed
from config.data import RuTexts


class PaymentConfig:
    payment_cb = "payment_callback"
    back_to_menu_cb = "back_to_menu"
    check_payment_crypto = "check_payment_crypto"
    check_payment_tinkoff = "check_payment_tinkoff"

    pay_crypto = "pay_type_crypto"
    pay_card = "pay_type_card"


class Callbacks:
    discord_cb = "btn_discord_callback"
    twitter_cb = "btn_twitter_callback"


def category_keyboard() -> InlineKeyboardMarkup:
    text_discord = _generate_text_for_inline_btn(RuTexts.discord, RuTexts.discord_account_price_usd)
    btn_discord = InlineKeyboardButton(text=f"{RuTexts.discord} {text_discord}",
                                       callback_data=Callbacks.discord_cb)
    text_twitter = _generate_text_for_inline_btn(RuTexts.twitter, RuTexts.twitter_account_price_usd)
    btn_twitter = InlineKeyboardButton(text=f"{RuTexts.twitter} {text_twitter}",
                                       callback_data=Callbacks.twitter_cb)

    keyboard = [[btn_discord],
                [btn_twitter]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


async def payment_type_keyboard(total_sum: float, tg_id: int, desc: str, goods_name: str, goods_count: int) -> InlineKeyboardMarkup:
    # CRYPTO PAY:

    load_dotenv()
    CRYPTO_TOKEN: str = os.getenv("CRYPTO_TOKEN")
    crypto = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.MAIN_NET)

    total_sum = 0.013  # для теста поставил копеечку, эту строку удалить

    invoice = await crypto.create_invoice(asset='USDT', amount=total_sum)
    invoice_url = invoice.bot_invoice_url
    invoice_id = invoice.invoice_id

    if not invoice_url:
        raise ValueError("Invoice url not found")
    btn1 = InlineKeyboardButton(text="Криптой",
                                url=invoice_url)
    btn2 = InlineKeyboardButton(text="Проверка оплаты (crypto)",
                                callback_data=f"invoice_id={invoice_id}")

    # ТИНЬКОФФ:

    # payment_data = create_pay_link(total_sum * 90, tg_id, desc, goods_name, goods_count)
    payment_data = ["https://google.com/", "payment_id"]

    btn3 = InlineKeyboardButton(text="Картой (РУБ)",
                                url=payment_data[0])
    btn4 = InlineKeyboardButton(text="Проверка оплаты (картой)",
                                callback_data=f"payment_id={payment_data[1]}")
    btn5 = InlineKeyboardButton(text="Вернуться в меню",
                                callback_data=PaymentConfig.back_to_menu_cb)

    keyboard = [[btn1, btn2], [btn3, btn4], [btn5]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await crypto.close()
    return markup


def _generate_text_for_inline_btn(category: str, price: float):
    return f"({_get_count_of_accounts(category)}) | ${price}"


async def make_payment_markup() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(text="Оплатить",
                                callback_data=PaymentConfig.payment_cb)
    btn2 = InlineKeyboardButton(text="Вернуться в меню",
                                callback_data=PaymentConfig.back_to_menu_cb)

    keyboard = [[btn1, btn2]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return markup


def _get_count_of_accounts(type: str):
    from .cb_handlers import _get_accounts_path
    match(type):
        case RuTexts.discord:
            path = _get_accounts_path("discord_accounts.txt", "../../config")
            with open(path) as file:
                count = len(file.readlines())
            return count
        case RuTexts.twitter:
            path = _get_accounts_path("twitter_accounts.txt", "../../config")
            with open(path) as file:
                count = len(file.readlines())
            return count

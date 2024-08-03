import os
import aiohttp
import aiohttp.http_exceptions
from dotenv import load_dotenv

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config.data import RuTexts


class PaymentConfig:
    payment_cb = "payment_callback"
    back_to_menu_cb = "back_to_menu"

    pay_crypto = "pay_type_crypto"
    pay_card = "pay_type_card"


class Callbacks:
    discord_cb = "btn_discord_callback"
    twitter_cb = "btn_twitter_callback"


def category_keyboard() -> InlineKeyboardMarkup:
    text_discord = _generate_text_for_inline_btn(RuTexts.discord, RuTexts.discord_account_price)
    btn_discord = InlineKeyboardButton(text=f"{RuTexts.discord} {text_discord}",
                                       callback_data=Callbacks.discord_cb)
    text_twitter = _generate_text_for_inline_btn(RuTexts.twitter, RuTexts.twitter_account_price)
    btn_twitter = InlineKeyboardButton(text=f"{RuTexts.twitter} {text_twitter}",
                                       callback_data=Callbacks.twitter_cb)

    keyboard = [[btn_discord],
                [btn_twitter]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


async def payment_type_keyboard(total_sum: float) -> InlineKeyboardMarkup:
    load_dotenv()
    CRYPTO_TOKEN: str = os.getenv("CRYPTO_TOKEN")

    headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
    async with aiohttp.ClientSession(headers=headers) as client:
        data = {
            "asset": "USDT",
            "amount": str(total_sum),
            "description": "Buy accounts [ucryptomarket]"
        }
        async with client.post("https://pay.crypt.bot/api/createInvoice", json=data) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                invoice_url = resp_json.get("result").get("pay_url")

    if not invoice_url:
        raise ValueError("Invoice url not found")
    btn1 = InlineKeyboardButton(text="Криптой",
                                url=invoice_url)
    btn2 = InlineKeyboardButton(text="Картой (РУБ)",
                                url="https://google.com")  # будет тинькоф
    btn3 = InlineKeyboardButton(text="Вернуться в меню",
                                callback_data=PaymentConfig.back_to_menu_cb)

    keyboard = [[btn1, btn2, btn3]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
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

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from config.data import RuTexts


class PaymentConfig:
    payment_cb = "payment_callback"
    back_to_menu_cb = "back_to_menu"


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


def _generate_text_for_inline_btn(category: str, price: float):
    return f"({_get_count_of_accounts(category)}) | ${price}"


def payment_markup() -> InlineKeyboardMarkup:
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

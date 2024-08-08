from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.data import RuTexts


class ReplaceAccountConfig:
    discord = "replace_discord_account"
    twitter = "replace_twitter_account"


def keyboard_discord_twitter_back() -> InlineKeyboardMarkup:
    btn_discord = InlineKeyboardButton(text=RuTexts.discord,
                                       callback_data=ReplaceAccountConfig.discord)
    btn_twitter = InlineKeyboardButton(text=RuTexts.twitter,
                                       callback_data=ReplaceAccountConfig.twitter)
    btn_back = InlineKeyboardButton(text="Назад↩️",
                                    callback_data="back")

    keyboard = [[btn_discord, btn_twitter], [btn_back]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return markup


def keyboard_back() -> InlineKeyboardMarkup:
    btn_back = InlineKeyboardButton(text="Назад↩️",
                                    callback_data="back")

    keyboard = [[btn_back]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return markup

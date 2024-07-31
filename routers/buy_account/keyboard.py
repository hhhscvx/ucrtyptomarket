from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.data import RuTexts


def category_keyboard() -> ReplyKeyboardMarkup:
    btn_discord = KeyboardButton(text=RuTexts.discord)
    btn_twitter = KeyboardButton(text=RuTexts.twitter)

    keyboard = [[btn_discord],
                [btn_twitter]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard,
                                 resize_keyboard=True)
    return markup

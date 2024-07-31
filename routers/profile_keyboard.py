from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.data import RuTexts


def profile_keyboard() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text=RuTexts.show_balance)
    btn2 = KeyboardButton(text=RuTexts.deposit_balance)
    btn3 = KeyboardButton(text=RuTexts.order_history)
    btn4 = KeyboardButton(text=RuTexts.our_channel)

    keyboard = [[btn1, btn2],
                [btn3, btn4]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard,
                                 resize_keyboard=True)
    return markup

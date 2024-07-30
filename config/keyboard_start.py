from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_start_keyboard() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text="")
    btn2 = KeyboardButton(text="")
    btn3 = KeyboardButton(text="")
    btn_profile = KeyboardButton(text="")
    btn4 = KeyboardButton(text="")
    btn5 = KeyboardButton(text="")
    btn6 = KeyboardButton(text="")

    keyboard = [[btn1, btn2, btn3],
                [btn_profile],
                [btn4, btn5, btn6]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    return markup

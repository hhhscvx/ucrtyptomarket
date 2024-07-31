from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .data import RuTexts


def start_keyboard() -> ReplyKeyboardMarkup:
    btn_categories = KeyboardButton(text=RuTexts.categories)
    btn_in_stock = KeyboardButton(text=RuTexts.in_stock)
    btn_about_us = KeyboardButton(text=RuTexts.about_us)
    btn_profile = KeyboardButton(text=RuTexts.profile)
    btn_replace = KeyboardButton(text=RuTexts.replacement_guarantee)
    btn_faq = KeyboardButton(text=RuTexts.faq)
    btn_support = KeyboardButton(text=RuTexts.support)

    keyboard = [[btn_categories, btn_in_stock, btn_about_us],
                [btn_profile],
                [btn_replace, btn_faq, btn_support]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard,
                                 resize_keyboard=True)
    return markup

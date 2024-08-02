from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_orders_history_keyboard(orders) -> InlineKeyboardMarkup:
    keyboard = []

    for order in orders:
        date = order['created'].split()[0]
        amount = order['amount']
        btn = [InlineKeyboardButton(f"{date}: {order['account_type']} [{amount} шт.]")]
        keyboard.append(btn)

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup

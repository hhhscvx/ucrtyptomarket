from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_orders_history_keyboard(orders) -> InlineKeyboardMarkup:
    keyboard = []

    for order in orders:
        date = order['created'].split()[0]
        amount = order['amount']
        uuid = order["uuid"]
        btn = [InlineKeyboardButton(text=f"{date}: {order['account_type']} [{amount} шт.]", callback_data=f"uuid={uuid}")]
        keyboard.append(btn)

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup

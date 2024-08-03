from aiogram.fsm.state import StatesGroup, State


class BuyAccount(StatesGroup):
    category = State()
    amount = State()
    pay_or_leave = State()
    payment_type = State()

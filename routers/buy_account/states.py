from aiogram.fsm.state import StatesGroup, State


class BuyAccount(StatesGroup):
    category = State()
    amount = State()

from aiogram.fsm.state import StatesGroup, State


class ReplaceAccount(StatesGroup):
    account_type = State()
    accounts_count = State()
    accounts = State()

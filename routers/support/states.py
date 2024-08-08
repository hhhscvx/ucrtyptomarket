from aiogram.fsm.state import StatesGroup, State


class SupportState(StatesGroup):
    question = State()

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount
from config.data import RuTexts


router = Router(name=__name__)

categories = [RuTexts.discord, RuTexts.twitter]


@router.message(BuyAccount.category, lambda message: message.text in categories)
async def handle_buy_account_category(message: Message, state: FSMContext):
    await message.answer(text=f"<b>{message.text}</b>\nВведите желаемое кол-во аккаунтов:",
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(category=message.text)
    await state.set_state(BuyAccount.amount)


@router.message(BuyAccount.category)
async def handle_buy_account_category_invalid(message: Message, state: FSMContext):
    await message.answer(f"Это значение недоступно. Пожалуйста, выберите значение на клавиатуре")

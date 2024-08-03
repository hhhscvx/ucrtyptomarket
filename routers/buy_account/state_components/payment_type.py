from aiogram import F, Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount
from ..keyboards import PaymentConfig
from config.data import get_accounts_count


router = Router(name=__name__)


# @router.callback_query(F.data == PaymentConfig.crypto, BuyAccount.payment_type)
# async def handle_buy_account_category(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     data = await state.update_data(payment_type=callback.data)
#     await callback.message.answer(text=f"<b>{categories[callback.data]}</b>\nВведите желаемое кол-во аккаунтов: (1-{accounts_count})",
#                                   reply_markup=ReplyKeyboardRemove())
#     await state.set_state(BuyAccount.amount)


# @router.callback_query(F.data == PaymentConfig.card, BuyAccount.payment_type)
# async def handle_buy_account_category(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     data = await state.update_data(payment_type=callback.data)
#     await callback.message.answer(text=f"<b>{categories[callback.data]}</b>\nВведите желаемое кол-во аккаунтов: (1-{accounts_count})",
#                                   reply_markup=ReplyKeyboardRemove())
#     await state.set_state(BuyAccount.amount)

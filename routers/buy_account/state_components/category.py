from aiogram import F, Router
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from routers.buy_account.states import BuyAccount
from ..keyboards import Callbacks
from config.data import RuTexts, get_accounts_count


router = Router(name=__name__)

categories = {Callbacks.discord_cb: RuTexts.discord,
              Callbacks.twitter_cb: RuTexts.twitter}


@router.callback_query(BuyAccount.category, lambda cb: cb.data in categories.keys())
async def handle_buy_account_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.update_data(category=categories[callback.data])
    accounts_count = get_accounts_count(data['category'].lower(), "../../config")
    await callback.message.answer(text=f"<b>{categories[callback.data]}</b>\nВведите желаемое кол-во аккаунтов: (1-{accounts_count})",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(BuyAccount.amount)

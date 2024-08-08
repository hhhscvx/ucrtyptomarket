from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from config.data import RuTexts
from config.keyboard_start import start_keyboard
from .keyboards import ReplaceAccountConfig
from .states import ReplaceAccount

router = Router(name=__name__)


@router.callback_query(F.data == 'back')
async def back_to_menu_from_replacement(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(RuTexts.START_MESSAGE, reply_markup=start_keyboard())


accounts_type = [ReplaceAccountConfig.discord, ReplaceAccountConfig.twitter]


@router.callback_query(lambda callback: callback.data in accounts_type, ReplaceAccount.account_type)
async def replace_discord_account(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    account_type = RuTexts.discord if callback.data == ReplaceAccountConfig.discord else RuTexts.twitter
    await state.update_data(account_type=account_type)
    await state.set_state(ReplaceAccount.accounts_count)
    await callback.message.answer(f"<b>{account_type}</b>\nВведите количество аккаунтов, которые вы хотите заменить")

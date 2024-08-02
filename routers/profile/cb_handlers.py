from aiogram import F, Router
from aiogram.types import CallbackQuery


router = Router(name=__name__)


@router.callback_query()
def return_order_by_hash(callback: CallbackQuery):
    # ЛОГИКА, КОТОРАЯ БЕРЕТ order ИЗ БАЗЫ ПО ХЭШУ В F.DATA
    # (ДОБАВЛЯЮ В ORDER ЕЩЕ ОДНУ КОЛОНКУ - ХЭШ и передаю его
    # в генерацию inline клавиатуры и отправляю callback кнопке, равный хэшу данного заказа)
    ...

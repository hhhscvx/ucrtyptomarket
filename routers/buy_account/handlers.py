from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .states import BuyAccount

from config.data import RuTexts
from .keyboards import category_keyboard, make_payment_markup
from .state_components.category import router as category_router
from .state_components.amount import router as amount_router

router = Router(name=__name__)
router.include_router(category_router)
router.include_router(amount_router)


@router.message(F.text == RuTexts.categories)
async def categories_message_handler(message: Message, state: FSMContext):
    await state.set_state(BuyAccount.category)
    await message.answer(text=message.text,
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text=RuTexts.choose_category,
                         reply_markup=category_keyboard())


async def send_order(message: Message, data: dict):
    category = data['category']
    price = RuTexts.twitter_account_price_usd if category == RuTexts.twitter else RuTexts.discord_account_price_usd
    amount = data['amount']
    total = price * float(amount)
    text = (f"<i><b>👀 Ваш заказ:</b></i>\n\n"
            f"Тип аккаунта: <b>{category}</b>\n"
            f"Количество: <code>{amount}</code>\n\n"
            f"<b>Цена:</b> {total}$")

    await message.answer(text=text, reply_markup=await make_payment_markup())

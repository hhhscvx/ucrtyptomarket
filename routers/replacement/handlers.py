from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config.data import RuTexts, get_accounts_count
from .keyboards import keyboard_discord_twitter_back, keyboard_back
from .states import ReplaceAccount
from .services import send_accounts_and_delete_sold
from database import fetchall


router = Router(name=__name__)


@router.message(F.text == RuTexts.replacement_guarantee)
async def replacement_message_handler(message: Message, state: FSMContext):
    text = "Выберите тип аккаунта для замены:"
    await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
    await message.answer(text=text, reply_markup=keyboard_discord_twitter_back())
    await state.set_state(ReplaceAccount.account_type)


@router.message(ReplaceAccount.accounts_count, lambda message: message.text.isdigit())
async def receive_accounts_count(message: Message, state: FSMContext):
    # ПРОВЕРКА ЧТО СТОЛЬКО АККОВ ВООБЩЕ ЕСТЬ
    data = await state.get_data()
    category = data['account_type'].lower()
    accounts_count = get_accounts_count(category, "../../config")
    if int(message.text) > accounts_count:
        await message.answer(f"К сожалению, у нас пока нет столько аккаунтов для замены. Пожалуйста, введите допустимое число: 1-{accounts_count}")
        return

    await state.update_data(accounts_count=message.text)
    await state.set_state(ReplaceAccount.accounts)
    text = "Введите аккаунты, которые хотите заменить в формате: <code>почта:пароль:токен\nпочта:пароль:токен</code>"
    await message.answer(text=text)


@router.message(ReplaceAccount.accounts_count)
async def receive_accounts_count_invalid(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите корректное число")


@router.message(ReplaceAccount.accounts)
async def receive_accounts(message: Message, state: FSMContext):
    acc_format = "<code>почта:пароль:токен\nпочта:пароль:токен\n</code>"
    data = await state.get_data()
    if message.text.count(":") != int(data['accounts_count']) * 2:
        await message.answer(f"Пожалуйста, введите корректно аккаунты ({data['accounts_count']} шт.) в формате: {acc_format}")
    else:
        first_acc = message.text.split('\n')[0]
        condition = f" AND buyer_tg_id = '{message.from_user.id}' AND account_type = '{data['account_type'].lower()}';"
        order = fetchall("orders", ['id'], f"WHERE accounts LIKE '%{first_acc}%'{condition}")
        replacements_accounts = fetchall("replacements", ["id"], f"WHERE replacement_accounts LIKE '%{first_acc}%'{condition}")
        received_accounts = fetchall("replacements", ["id"], f"WHERE received_accounts LIKE '%{first_acc}%'{condition}")

        if (not order) and (not received_accounts):
            await message.answer(f"Пожалуйста, введите аккаунты, которые вы покупали у нас)", reply_markup=keyboard_back())
        elif replacements_accounts:
            await message.answer(f"Какой(ие)-то из этих аккаунтов вы уже заменяли. Попробуйте еще раз", reply_markup=keyboard_back())
        else:
            amount_accounts = int(data['accounts_count'])
            account_category = data['account_type']
            match(account_category):
                case RuTexts.discord:
                    await send_accounts_and_delete_sold(acc_type=RuTexts.discord, message=message,
                                                        amount_accounts=amount_accounts, replacement_accounts=message.text)
                case RuTexts.twitter:
                    await send_accounts_and_delete_sold(acc_type=RuTexts.twitter, message=message,
                                                        amount_accounts=amount_accounts, replacement_accounts=message.text)
            await state.clear()

import os
from aiogram.types.input_file import FSInputFile
from aiogram.types import Message

from config.data import RuTexts
from database import insert

# похуй возьму наверно щас все сюда скопирую (все методы) и перепишу под message, а не callback


def _get_accounts_path(filename: str, location: str) -> str:
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, location)
    accounts_file_path = os.path.join(config_dir, filename)
    return accounts_file_path


def _get_accounts(count: int, accounts: list) -> str:
    res = ''
    for i in range(count):
        res += f"{accounts[i]}\n"
    return res


async def _send_accounts(message: Message, accounts: list, amount_accounts: int) -> None:
    file_path = f"accounts_{message.from_user.id}"
    with open(file_path, "w") as file:
        file.writelines(_get_accounts(amount_accounts, accounts))
    await message.answer_document(FSInputFile(file_path),
                                  caption="Ваши аккаунты готовы!\n\nФормат: почта:пароль:токен")
    os.remove(file_path)


async def send_accounts_and_delete_sold(acc_type: str, message: Message, amount_accounts: int, replacement_accounts: str):
    match(acc_type):
        case RuTexts.discord:
            await send_accounts(message=message, account_type='discord',
                                amount_accounts=amount_accounts, replacement_accounts=replacement_accounts)
        case RuTexts.twitter:
            await send_accounts(message=message, account_type='twitter',
                                amount_accounts=amount_accounts, replacement_accounts=replacement_accounts)


async def send_accounts(message: Message, account_type: str, amount_accounts, replacement_accounts: str):
    file_path = _get_accounts_path(f'{account_type}_accounts.txt', '../../config')
    with open(file_path, 'r') as file:
        accounts = list(map(lambda string: string.rstrip('\n'), file.readlines()))
        await _send_accounts(message=message, accounts=accounts, amount_accounts=amount_accounts)
        print('REPLACEMENT ACCOUNT FROM send_accounts:')
        print(replacement_accounts)
        _save_order_to_db(message, account_type, replacement_accounts,
                          received_accounts="\n".join(accounts[:amount_accounts]))
    with open(file_path, 'w') as file:
        file.writelines(
            map(lambda string: f"{string}\n" if not accounts[-1] == string else string, accounts[amount_accounts:]))


def _save_order_to_db(message: Message, account_type: str, replacement_accounts: str, received_accounts: str):
    buyer_tg_id = message.from_user.id
    insert(table="replacements", column_values={
        "buyer_tg_id": buyer_tg_id,
        "account_type": account_type,
        "replacement_accounts": replacement_accounts,
        "received_accounts": received_accounts,
    })

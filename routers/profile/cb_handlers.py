import os
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types.input_file import FSInputFile

from database import fetchall


router = Router(name=__name__)


@router.callback_query(F.data.startswith("uuid="))
async def return_order_by_hash(callback: CallbackQuery):
    uuid = callback.data.split("=")[1]
    order = fetchall("orders",
                     ['created', 'account_type', 'amount', 'accounts'],
                     f"WHERE uuid = '{uuid}'")[0]
    
    if not order:
        return

    await callback.answer()
    text = (f"<i>Заказ от {order['created']}</i>\n"
            f"Аккаунты: <b>{order['account_type']} [{order['amount']} шт.]</b>")
    file_path = f"accounts_{uuid}"
    with open(file_path, 'w') as file:
        file.writelines(order['accounts'])
    await callback.message.answer_document(document=FSInputFile(file_path),
                                            caption=text)
    os.remove(file_path)

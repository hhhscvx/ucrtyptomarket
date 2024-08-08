# import hashlib

# import requests

# from config import payment_password, payment_merchant_id
# import utils

# api_address = "https://securepay.tinkoff.ru/v2"
# #api_address = "https://rest-api-test.tinkoff.ru/v2"


# def create_payment_signature(**params: str) -> str:
#     """
#     Создаёт подпись запроса, необходимую
#     :param params: Передаются все параметры, которые передаются в запросе
#     :return: Подпись запроса
#     """
#     data = {"TerminalKey": payment_merchant_id,
#             "Password": payment_password,
#             **params
#             }

#     # noinspection PyTypeChecker
#     data = dict(sorted(data.items()))
#     data = "".join(data.values())
#     data = hashlib.sha256(data.encode()).hexdigest()
#     return data


# def create_pay_link(price: int, tg_id: int, desc: str, goods_name: str, goods_count: int) -> tuple:
#     """
#     Создаёт платёжную ссылку,
#     :param price: Цена
#     :param tg_id: айди пользователя в системе телеграм
#     :param desc: Описание товара, отображается при проведении юзером оплаты
#     :return: ссылка для оплаты, подпись запроса, айди платежа в системе тинькофф
#     """
#     order_id = utils.create_order(tg_id=tg_id)

#     price *= 100  # Платёжка принимает сумму в копейках, переводим в рубли
#     payment_signature = create_payment_signature(Amount=str(price),
#                                                  Description=desc,
#                                                  OrderId=order_id)

#     req_data = {
#             "TerminalKey": payment_merchant_id,  # string
#             "Amount": price,
#             "OrderId": order_id,  # String
#             "Description": desc,
#             "Token": payment_signature,
#             "DATA": {
#                 "telegram_id": str(tg_id)
#             },
#             "Receipt": {
#                 "Email": "kuricinyopta@mail.ru", # это чекуть еще че это в доке
#                 "Phone": "79511925584",
#                 "Taxation": "usn_income",
#                 "Items": [
#                     {
#                         "Name": goods_name,
#                         "Price": price,
#                         "Quantity": goods_count,
#                         "Amount": price,
#                         "Tax": "none",
#                     }
#                 ]
#             }
#     }

#     response = requests.post(f"{api_address}/Init",
#                              headers={
#                                  "Content-Type": "application/json"
#                              },
#                              json=req_data
#                              )

#     response = response.json()
#     pay_link = response["PaymentURL"]
#     payment_id = response["PaymentId"]

#     utils.update_payment_order(order_id, payment_id)
#     return pay_link, payment_id, order_id


# def check_order_payed(payment_id) -> bool:
#     """
#     :param payment_id: Айди платежа в платёжной системе тинькофф, возвращается при создании ссылки для оплаты
#     :return: True/False оплачено/не оплачено
#     """

#     payment_signature = create_payment_signature(
#         PaymentId=payment_id,
#     )

#     response = requests.post(f"{api_address}/GetState",
#                              headers={
#                                  "Content-Type": "application/json"
#                              },
#                              json={
#                                  "TerminalKey": payment_merchant_id,
#                                  "Token": payment_signature,
#                                  "PaymentId": payment_id
#                              }).json()

#     if response.get("Status") == "CONFIRMED":
#         return True
#     return False
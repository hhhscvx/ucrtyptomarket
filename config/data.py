
class RuTexts:
    START_MESSAGE = "Привет! Я здесь, чтобы помочь вам покупать и продавать аккаунты Discord и Twitter безопасно и легко. Я ваш персональный рыночный бот, предлагающий широкий выбор аккаунтов, которые помогут вам расширить свое присутствие в социальных сетях и достичь ваших маркетинговых целей."

    categories = "Все категории"
    in_stock = "В наличии"
    about_us = "О нас"
    profile = "Профиль"
    replacement_guarantee = "Гарантия замены"
    faq = "FAQ"
    support = "Поддержка"

    show_balance = "Отобразить баланс"
    deposit_balance = "Пополнить баланс"
    order_history = "Прошлые заказы"
    our_channel = "Наш канал"

    choose_category = "Выберите категорию"
    enter_amount = "Введите количество"

    discord = "Discord"
    discord_account_price = 0.25
    twitter = "Twitter"
    twitter_account_price = 0.79


# хапхапвх у меня уже был такой метод ну лан)
def get_accounts_count(category: str, accounts_path: str) -> int:
    from routers.buy_account.cb_handlers import _get_accounts_path
    path = _get_accounts_path(f"{category}_accounts.txt", accounts_path)
    with open(path, 'r') as file:
        accounts_count = len(file.readlines())
    return accounts_count

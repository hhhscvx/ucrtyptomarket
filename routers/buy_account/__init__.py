__all__ = ("router", )

from aiogram import Router

from .handlers import router as account_router
from .cb_handlers import router as cb_account_router
from .payment_cb_handlers import router as payment_cb_handlers

router = Router()

router.include_routers(account_router,
                       payment_cb_handlers,
                       cb_account_router)

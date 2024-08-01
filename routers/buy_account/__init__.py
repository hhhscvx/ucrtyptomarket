__all__ = ("router", )

from aiogram import Router

from .handlers import router as account_router
from .cb_handlers import router as cb_account_router

router = Router()

router.include_routers(account_router,
                       cb_account_router)

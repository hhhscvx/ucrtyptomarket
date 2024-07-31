__all__ = ("router", )

from aiogram import Router

from .keyboard_response import router as kb_response_router
from .commands import router as commands_router
from .buy_account import router as account_router

router = Router(name=__name__)


router.include_routers(kb_response_router,
                       account_router,
                       commands_router)

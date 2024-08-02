__all__ = ("router", )

from aiogram import Router

from .commands import router as commands_router
from .buy_account import router as account_router
from .profile import router as profile_router

router = Router(name=__name__)


router.include_routers(profile_router,
                       account_router,
                       commands_router)

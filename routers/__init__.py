__all__ = ("router", )

from aiogram import Router

from .commands import router as commands_router
from .buy_account import router as account_router
from .profile import router as profile_router
from .replacement import router as replacement_router
from .support import router as support_router

router = Router(name=__name__)


router.include_routers(commands_router,
                       support_router,
                       replacement_router,
                       account_router)

# last !
router.include_router(profile_router)

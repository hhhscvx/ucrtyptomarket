__all__ = ("router", )

from aiogram import Router

from .handlers import router as handlers_router
from .cb_handlers import router as cb_handlers_router

router = Router()

router.include_routers(handlers_router,
                       cb_handlers_router)

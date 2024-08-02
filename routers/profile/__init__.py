__all__ = ("router", )

from aiogram import Router

from .handlers import router as handle_router

router = Router(name=__name__)

router.include_routers(handle_router)

__all__ = ("router", )

from aiogram import Router

from .handlers import router as account_router

router = Router()

router.include_router(account_router)

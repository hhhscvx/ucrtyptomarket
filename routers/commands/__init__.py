__all__ = ("router", )

from aiogram import Router

from .base_commands import router as base_cmds_router

router = Router()

router.include_router(base_cmds_router)

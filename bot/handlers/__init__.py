# bot/handlers/__init__.py
from .common import router as common_router
from .fitness import router as fitness_router

__all__ = ["common_router", "fitness_router"]
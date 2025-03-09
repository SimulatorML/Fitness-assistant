from fastapi import APIRouter

router = APIRouter()

from . import users
from . import activities
router.include_router(users.router)
router.include_router(activities.router)
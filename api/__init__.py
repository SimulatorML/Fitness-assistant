from fastapi import APIRouter
from .routers.users import router as users_router
from .routers.activities import router as activities_router
from .routers.llm import router as llm_router

router = APIRouter()
router.include_router(users_router)
router.include_router(activities_router)
router.include_router(llm_router)

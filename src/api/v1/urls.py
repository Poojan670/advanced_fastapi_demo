from fastapi import APIRouter
from src.user.routes import user

router = APIRouter()
router.include_router(user.router, prefix="/user-app", tags=["user"])

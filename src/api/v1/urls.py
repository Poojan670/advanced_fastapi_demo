from fastapi import APIRouter
from src.user.routes import user
from src.user.routes import login

router = APIRouter()
router.include_router(user.router, prefix="/user-app", tags=["user"])
router.include_router(login.router, prefix="/user-app", tags=["user"])

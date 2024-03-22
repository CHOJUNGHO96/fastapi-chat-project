from fastapi import APIRouter

from app.auth.routes import auth_api_router
from app.chat.routes import chat_api_router


router = APIRouter()


router.include_router(auth_api_router, prefix="/auth")
router.include_router(chat_api_router, prefix="/chat")

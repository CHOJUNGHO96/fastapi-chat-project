from fastapi import APIRouter

from app.auth.endpoint.login import router as login

from app.chat.endpoint.chat import router as chat

router = APIRouter()

router.include_router(login, prefix="/auth", tags=["로그인"])
router.include_router(chat, prefix="/chat", tags=["채팅"])

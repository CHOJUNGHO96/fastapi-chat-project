from fastapi import APIRouter

import app.chat.endpoint.chat as chat

chat_api_router = APIRouter()
chat_api_router.include_router(chat.router, tags=["chat"])

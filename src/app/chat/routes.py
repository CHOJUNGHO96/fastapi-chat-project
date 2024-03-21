from fastapi import APIRouter

import app.chat.endpoint.chat as chat

auth_api_router = APIRouter()
auth_api_router.include_router(chat.router, tags=["chat"])

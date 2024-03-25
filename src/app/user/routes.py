from fastapi import APIRouter

import app.user.endpoint.friendship as friendship

friendship_api_router = APIRouter()
friendship_api_router.include_router(friendship.router, tags=["user"])

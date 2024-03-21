from fastapi import APIRouter

import app.auth.endpoint.login as login

auth_api_router = APIRouter()
auth_api_router.include_router(login.router, tags=["Authentication"])

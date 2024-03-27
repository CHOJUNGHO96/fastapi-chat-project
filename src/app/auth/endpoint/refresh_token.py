from dependency_injector.wiring import inject
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.auth.domain.user_model import ModelTokenData
from app.auth.usecase.authentication import get_token, save_user_in_redis

router = APIRouter()


@router.get("/refresh_token")
@inject
async def refresh_token(
    request: Request,
):
    if "refresh_token" in request.cookies:
        token_data: ModelTokenData = await get_token(request, user_info=request.state.user)
        await save_user_in_redis(request.state.user, token_data)
        response = JSONResponse(content=token_data.dict())
        response.set_cookie("token_type", token_data.token_type)
        response.set_cookie("access_token", token_data.access_token)
        response.set_cookie("refresh_token", token_data.refresh_token)
        return response
    else:
        return JSONResponse(status_code=422, content={"status": 422, "msg": "Token not in cookie"})

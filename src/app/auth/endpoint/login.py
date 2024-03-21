from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.domain.user_model import ModelTokenData
from app.auth.usecase.authentication import authenticate, get_token, save_user_in_redis

router = APIRouter()


@router.post("/login", response_model=ModelTokenData)
@inject
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> JSONResponse:
    user_info = await authenticate(user_id=form_data.username, user_passwd=form_data.password)
    token_data: ModelTokenData = await get_token(request, user_info=user_info)
    await save_user_in_redis(user_info, token_data)
    response = JSONResponse(content=token_data.dict())
    response.set_cookie("token_type", token_data.token_type)
    response.set_cookie("access_token", token_data.access_token)
    response.set_cookie("refresh_token", token_data.refresh_token)

    return response

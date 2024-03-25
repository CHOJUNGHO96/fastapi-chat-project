from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.auth.domain.user_model import ModelUserRegister
from app.auth.services.user_service import Service as UserService
from app.auth.usecase.authentication import check_user, set_hash_pawssowrd

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
@inject
async def registration(
    user_info: ModelUserRegister,
    user_service: UserService = Depends(Provide["auth.user_service"]),
) -> JSONResponse:
    if await check_user(user_info):
        user_info.password = await set_hash_pawssowrd(user_info.password)
        result = await user_service.create_user(user_info)
        return JSONResponse(content={"status": 200, "msg": "Success Register.", "code": 200, "list": [result]})
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "Fail to register", "code": 422, "list": []}
        )

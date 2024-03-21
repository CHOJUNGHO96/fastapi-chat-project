from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.auth.domain.user_model import ModelUserRegister
from app.auth.usecase.authentication import check_user
from app.auth.services.user_service import Service as UserService
from app.auth.usecase.authentication import set_hash_pawssowrd

router = APIRouter()


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

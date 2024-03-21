# coding=utf-8
from dependency_injector.wiring import Provide, inject
from fastapi import Request
from passlib.context import CryptContext

from app.auth.domain.user_model import ModelTokenData, ModelUserRegister
from app.auth.services.user_service import Service as UserService
from app.auth.util.jwt import create_access_token
from errors import BadPassword, NotFoundUserEx, DuplicateUserEx
from infrastructure.db.schema.user import UserInfo


async def set_hash_pawssowrd(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        raise BadPassword()


@inject
async def get_token(
    request: Request,
    user_info: UserInfo,
    config=Provide["config"],
) -> ModelTokenData:
    request.state.user = user_info
    token_type = "bearer"
    access_token = create_access_token(
        jwt_secret_key=config["JWT_ACCESS_SECRET_KEY"],
        jwt_algorithm=config["JWT_ALGORITHM"],
        user_id=user_info.user_id,
        login_id=user_info.login_id,
        user_name=user_info.user_name,
        user_type=user_info.user_type,
        expire=config["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"],
    )
    refresh_token = create_access_token(
        jwt_secret_key=config["JWT_REFRESH_SECRET_KEY"],
        jwt_algorithm=config["JWT_ALGORITHM"],
        user_id=user_info.user_id,
        login_id=user_info.login_id,
        user_name=user_info.user_name,
        user_type=user_info.user_type,
        expire=config["JWT_REFRESH_TOKEN_EXPIRE_MINUTES"],
    )
    return ModelTokenData(
        user_id=user_info.user_id,
        token_type=token_type,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@inject
async def authenticate(
    user_id: str,
    user_passwd: str,
    user_service: UserService = Provide["auth.user_service"],
) -> UserInfo:
    user_info: UserInfo | None = await user_service.get_one(login_id=user_id)
    if not user_info:
        raise NotFoundUserEx()
    assert user_info.password, "password is invalid"
    if not await verify_password(user_passwd, user_info.password):
        assert user_info.login_id, "login_id is None"
        raise NotFoundUserEx()
    assert user_info.login_id is not None, "login_id is None"
    return user_info


@inject
async def save_user_in_redis(
    user_info: UserInfo,
    token_data: ModelTokenData,
    redis=Provide["redis"],
    config=Provide["config"],
) -> None:
    await redis.set(
        name=f"cahce_user_info_{user_info.login_id}",
        value=str(
            {
                "user_id": user_info.user_id,
                "login_id": user_info.login_id,
                "user_name": user_info.user_name,
                "email": user_info.email,
                "access_token": token_data.access_token,
                "refresh_token": token_data.refresh_token,
            }
        ),
        ex=config["REDIS_EXPIRE_TIME"],
    )


async def check_user(
    user_info: ModelUserRegister,
    user_service: UserService = Provide["auth.user_service"],
) -> bool:
    user_info: UserInfo | None = await user_service.get_one(login_id=user_info.login_id)
    if not user_info:
        return True
    else:
        raise DuplicateUserEx(user_id=user_info.login_id)

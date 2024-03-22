# coding=utf-8
from dependency_injector.wiring import Provide, inject


@inject
async def get_cahce_user(login_id, redis=Provide["redis"]) -> str:
    user_info = await redis.get(f"cahce_user_info_{login_id}")
    return await redis.get(f"cahce_user_info_{login_id}")

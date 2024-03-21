# coding=utf-8
from dependency_injector.wiring import Provide, inject

import errors
from app.auth.repository.user_repository import Repository as UserRepository
from infrastructure.db.schema.user import UserInfo


class Service:
    @inject
    async def get_one(
        self,
        user_repository: UserRepository = Provide["auth.user_repository"],
        **kwargs,
    ) -> UserInfo | None:
        where = []
        if kwargs.get("user_id"):
            where.append(UserInfo.user_id == kwargs["user_id"])
        if kwargs.get("login_id"):
            where.append(UserInfo.login_id == kwargs["login_id"])
        if kwargs.get("user_name"):
            where.append(UserInfo.user_name == kwargs["user_name"])
        user_info: UserInfo = await user_repository.one(*where)

        if not user_info:
            raise errors.NotFoundUserEx()

        return user_info

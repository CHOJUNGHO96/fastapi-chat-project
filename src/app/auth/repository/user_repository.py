# coding=utf-8
from contextlib import AbstractAsyncContextManager
from typing import Callable, Tuple, Any, List, Dict

from sqlalchemy import select, insert, Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.domain.user_model import ModelUserRegister
from errors import InternalQuerryEx
from infrastructure.db.schema.user import UserInfo


class Repository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

    async def one(self, *where) -> UserInfo | None:
        async with self.session_factory() as session:
            user_info = await session.scalars(select(UserInfo).where(*where))
            user_info = user_info.first()
            if not user_info:
                return None
            else:
                return user_info

    async def create_user(self, user_info: ModelUserRegister) -> list[dict[Any, Any]]:
        async with self.session_factory() as session:
            if user_info := await session.execute(
                insert(UserInfo)
                .values(**user_info.dict())
                .returning(UserInfo.login_id, UserInfo.user_name, UserInfo.email)
            ):
                user_info = user_info.first()
                return [{"login_id": user_info.login_id, "user_name": user_info.user_name, "email": user_info.email}]
            else:
                raise InternalQuerryEx()

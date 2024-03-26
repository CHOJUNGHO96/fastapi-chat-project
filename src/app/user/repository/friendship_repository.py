# coding=utf-8
from contextlib import AbstractAsyncContextManager
from typing import Any, Callable

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from errors import InternalQuerryEx
from infrastructure.db.schema.friendship import Friendship
from infrastructure.db.schema.user import UserInfo


class Repository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

    async def get_select_friendship(self, *where) -> list[dict[str, Any]] | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserInfo.user_name, UserInfo.login_id)
                .join(Friendship, Friendship.friend_id == UserInfo.user_id)
                .where(*where)
            )
            friend_info = result.fetchall()
            if not friend_info:
                return None
            else:
                return [{"user_name": f[0], "login_id": f[1]} for f in friend_info]

    async def register_friendship(self, **kwargs) -> bool:
        async with self.session_factory() as session:
            friend_id = await session.scalars(select(UserInfo.user_id).where(UserInfo.login_id == kwargs["friend_id"]))
            friend_id = friend_id.first()
            if await session.execute(
                insert(Friendship),
                [
                    {"user_id": kwargs["user_id"], "friend_id": friend_id},
                    {"user_id": friend_id, "friend_id": kwargs["user_id"]},
                ],
            ):
                return True
            else:
                raise InternalQuerryEx()

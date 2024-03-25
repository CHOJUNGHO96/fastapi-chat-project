# coding=utf-8
from contextlib import AbstractAsyncContextManager
from typing import Any, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

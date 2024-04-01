# coding=utf-8
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
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

    async def get_select_friendship(self, where) -> list[int]:
        async with self.session_factory() as session:
            result = await session.execute(select(UserInfo.user_id).where(UserInfo.login_id.in_(where)))
            # user_ids = result.scalars().all() scalars().all()은 각 행의 첫 번째 열 값을 반환하는 iterable을 제공
            user_ids = [row.user_id for row in result]
            result = await session.execute(
                select(Friendship.friendship_id).where(
                    (Friendship.user_id == user_ids[0]) & (Friendship.friend_id == user_ids[1])
                    | (Friendship.user_id == user_ids[1]) & (Friendship.friend_id == user_ids[0])
                )
            )
            friendship_dis = [row.friendship_id for row in result]
            if not result:
                raise InternalQuerryEx()
            else:
                return friendship_dis

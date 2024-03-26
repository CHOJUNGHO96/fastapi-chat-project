# coding=utf-8
from typing import Any

from dependency_injector.wiring import Provide, inject

from app.user.repository.friendship_repository import Repository as FriendShipRepository
from infrastructure.db.schema.friendship import Friendship


class Service:
    @inject
    async def get_select_friendship(
        self,
        friendship_repository: FriendShipRepository = Provide["user.friend_ship_repository"],
        **kwargs,
    ) -> list[dict[str, Any]]:
        where = []
        if kwargs.get("user_id"):
            where.append(Friendship.user_id == kwargs["user_id"])
        if kwargs.get("friend_id"):
            where.append(Friendship.friend_id.in_(kwargs["friend_id"]))

        friend_info: list[dict[str, Any]] = await friendship_repository.get_select_friendship(*where)

        return friend_info

    @inject
    async def register_friendship(
        self,
        friendship_repository: FriendShipRepository = Provide["user.friend_ship_repository"],
        **kwargs,
    ) -> bool:
        friend_info: bool = await friendship_repository.register_friendship(**kwargs)

        return friend_info

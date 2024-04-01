# coding=utf-8
from dependency_injector.wiring import Provide, inject

from app.chat.repository.friendship_repository import Repository as FriendshipRepository


class Service:
    @inject
    async def select(
        self,
        friendship_repository: FriendshipRepository = Provide["chat.friend_ship_repository"],
        **kwargs,
    ) -> list[int]:
        where = []
        if kwargs.get("login_id") and kwargs.get("recive_client_id"):
            where.extend([kwargs["login_id"], kwargs["recive_client_id"]])

        friendship_dis: list[int] = await friendship_repository.get_select_friendship(where)

        return friendship_dis

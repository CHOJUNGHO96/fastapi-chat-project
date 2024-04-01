# coding=utf-8
from dependency_injector import containers, providers

from app.chat.repository.friendship_repository import Repository as FriendShipRepository
from app.chat.services.friendship_service import Service as FriendShipService


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()

    # Service
    friend_ship_service = providers.Singleton(FriendShipService)

    # Repository
    friend_ship_repository = providers.Singleton(FriendShipRepository, session_factory=db.provided.session)

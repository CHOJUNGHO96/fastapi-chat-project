# coding=utf-8
from dependency_injector import containers, providers

from app.auth.repository.user_repository import Repository as UserRepository
from app.auth.services.user_service import Service as UserService


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()

    # Service
    user_service = providers.Singleton(UserService)

    # Repository
    user_repository = providers.Singleton(UserRepository, session_factory=db.provided.session)

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from authentication_service.repositories import AuthRepository


from settings import common_settings
from core.rabbit import create_rabbit_connection
from core.rabbit import create_rabbit_channel
from core.rabbit.depends import create_rabbit_async_instance
from authentication_service.controllers import AuthRabbitController, AuthUserController


class AuthServiceContainer(containers.DeclarativeContainer):
    # wiring_config прописывается в классе унаследованного контейнера в уникальном сервисе
    wiring_config = containers.WiringConfiguration(
        modules=["authentication_service.routers.auth_router",
                 "authentication_service.controllers.auth_users_controller",
                 ]
    )
    config = providers.Configuration()

    # зависимости для рэббита:
    rabbit_connection = providers.Factory(
        create_rabbit_connection,
        url=common_settings.RABBIT_URL
    )
    rabbit_channel = providers.Factory(
        create_rabbit_channel,
        connection=rabbit_connection,
    )
    rabbit_service = providers.Singleton(
        create_rabbit_async_instance,
        connection=rabbit_connection,
        ch=rabbit_channel,
    )

    # зависимости для работы с базой данных:
    engine = providers.Singleton(
        create_async_engine,
        url=common_settings.AUTH_SQL_SCHEMA,
        echo=True,
    )
    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async_session = providers.Factory(
        session_factory,
    )
    auth_repository = providers.Factory(
        AuthRepository,
        session_factory=async_session,
    )

    # контроллеры
    rabbit_controller = providers.Singleton(
        AuthRabbitController,
        rabbit=rabbit_service
    )
    auth_controller = providers.Factory(
        AuthUserController,
        session_maker=async_session,
        main_repository=auth_repository,
        rabbit=rabbit_controller
    )

    # rabbit_async_instance = providers.Factory(
    #     create_rabbit_async_instance,
    # )
    #
    # rabbit_service = providers.Singleton(
    #     RabbitAsyncRepository,
    #     connection=rabbit_connection,
    #     ch=rabbit_channel,
    #     queues_list=None,
    #     exchanges_list=[settings.aws.MY_SERVICE_EXCHANGE_NAME]
    # )

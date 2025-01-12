from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from users_service.repositories import UserRepository


from authentication_service.settings import common_settings
from core.rabbit import create_rabbit_connection
from core.rabbit import create_rabbit_channel
from core.rabbit.depends import create_rabbit_async_instance
from users_service.controllers import UserController, RabbitController


class UserServiceContainer(containers.DeclarativeContainer):
    # wiring_config прописывается в классе унаследованного контейнера в вашем сервисе
    # см пример my_service.depends.service_container
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
        url=common_settings.SQL_DSN,
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
    user_repository = providers.Factory(
        UserRepository,
        session_factory=async_session,
    )

    # контроллеры
    rabbit_controller = providers.Singleton(
        RabbitController,
        rabbit=rabbit_service
    )
    user_controller = providers.Factory(
        UserController,
        session_maker=async_session,
        main_repository=user_repository,
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

    wiring_config = containers.WiringConfiguration(
        modules=["users_service.routers.user_router",
                 "users_service.controllers.user_controller",
                 ]
    )

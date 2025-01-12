from core.rabbit import BaseSchemaForEvent, RabbitBase
from core.rabbit import RabbitControllerBase
from authentication_service.settings import common_settings


async def example_func(message: dict) -> None:
    pass


class AuthRabbitController(RabbitControllerBase):
    """
    Контроллер кролика для сервиса аутентификации.
    Два необходимых атрибута переопределены.
    """
    def __init__(self, rabbit: RabbitBase):
        super().__init__(rabbit=rabbit)
        self.exchange_to_send_own_event = common_settings.AUTHENTICATION_EVENT_EXCHANGE_NAME
        self.queue_and_exchange_event_schema = BaseSchemaForEvent(
            queue=common_settings.QUEUE_FOR_LISTEN_USERS_EVENT,
            function=example_func,
            depends_on_exchange=common_settings.NEW_USERS_EVENT_EXCHANGE_NAME
        )

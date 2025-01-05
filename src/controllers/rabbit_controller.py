from core.rabbit import BaseSchemaForEvent
from settings import common_settings
from typing import Literal, Optional
from pydantic import BaseModel
from core.logger import AppLogger
from core.rabbit import RabbitBase


async def do_something(message: dict) -> None:
    pass


class RabbitController:
    """
    Реализация контроллера, для сервиса my_service.
    Кролик инициализирует событие в обменник и слушает через одну очередь события от другого сервиса.
    """
    def __init__(
            self,
            rabbit: RabbitBase
    ):
        self.rabbit = rabbit
        self.new_user_event_exchange = None
        self.queue_for_listening_events_from_another_service = None
        self.model_for_other_service_event = BaseSchemaForEvent(
            queue=common_settings.QUEUE_FOR_OTHER_SERVICE_EVENT,
            function=do_something,
            depends_on_exchange=common_settings.OTHER_EVENT_EXCHANGE_NAME
        )

    async def init(self):
        """
        Метод инициализации всех очередей и обменников внутри контроллера ждя конткретного сервиса.
        У каждого сервиса набор и названия очередей/обменников свой.
        :return:
        """
        try:
            """
            пока так, т.к. не продумана логика янвного ожидания поднятия сервиса где объявляется обменник (обменника 
            может не быть, а очередь к нему подвязывается)
            эта проблема может быть легко решена путем создания сущности обменника в самом контроллере с целью только
            привязки очереди к обменнику, без использования контроллером обменника напрямую.
            """
            if not self.queue_for_listening_events_from_another_service:
                self.queue_for_listening_events_from_another_service = await self.rabbit.declare_queue(
                    queue_name=self.model_for_other_service_event.queue,
                    exchange_name=self.model_for_other_service_event.depends_on_exchange)
        except Exception as e:
            AppLogger.error(e.__str__())
            await self.rabbit.reconnect_channel()

        if not self.new_user_event_exchange:
            self.new_user_event_exchange = await self.rabbit.declare_exchange(
                exchange_name=common_settings.USERS_EVENT_EXCHANGE_NAME
            )

    async def consume_queue_for_events_from_another_service(self) -> None:
        """
        Метод - пример как настроить прослушку с внешнего сервиса ивентов.
        На каждый ивент нужна своя очередь в контроллере потребителя и отдельный метод прослушивания.
        """
        await self.init()
        await self.rabbit.consume_queue(
            queue_instance=self.queue_for_listening_events_from_another_service,
            do_something=self.model_for_other_service_event.function
        )

    async def publish_new_user_event(
            self,
            data_schema: BaseModel,
            convert_data_type: Optional[Literal['json']] = None
    ) -> None:
        """
        Метод публикации сообщения в обменник.
        :param exchange_name: имя обменника.
        :param data_schema: заполненные данные в виде схемы pydantic для отправки.
        :param convert_data_type: тип конвертации данных.
        :return: ничего.
        """
        async with self.rabbit.rabbitmq_async_connection:
            if not self.new_user_event_exchange:
                await self.init()

            to_send = data_schema
            if convert_data_type:
                to_send = self.rabbit.convert_data_to_message_sending_type(data_schema, convert_data_type)
            await self.new_user_event_exchange.publish(to_send, routing_key="info")

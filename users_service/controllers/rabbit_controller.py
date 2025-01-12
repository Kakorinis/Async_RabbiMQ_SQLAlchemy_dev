from core.rabbit import BaseSchemaForEvent, RabbitBase
from core.rabbit import RabbitControllerBase
from authentication_service.settings import common_settings


async def example_func(message: dict) -> None:
    pass


class RabbitController(RabbitControllerBase):
    """
    Контроллер кролика для сервиса пользователей.
    Два необходимых атрибута переопределены.
    """
    def __init__(self, rabbit: RabbitBase):
        super().__init__(rabbit=rabbit)
        self.exchange_to_send_own_event = common_settings.NEW_USERS_EVENT_EXCHANGE_NAME
        self.queue_and_exchange_event_schema = BaseSchemaForEvent(
            queue=common_settings.QUEUE_FOR_LISTEN_AUTHENTICATION_EVENT,
            function=example_func,
            depends_on_exchange=common_settings.AUTHENTICATION_EVENT_EXCHANGE_NAME
        )





# class RabbitController:
#     """
#     Реализация контроллера для сервиса users.
#     Кролик инициализирует событие в обменник и слушает через одну очередь события от другого сервиса.
#     Текущая реализация - контроллер может прослушивать только один обменник через спец. очередь для этого.
#     """
#     def __init__(
#             self,
#             rabbit: RabbitBase
#     ):
#         self.rabbit = rabbit
#         self.new_user_event_exchange = None
#         self.queue_for_listening_events_from_another_service = None
#         self.queue_and_exchange_event_schema = BaseSchemaForEvent(
#             queue=common_settings.QUEUE_FOR_LISTEN_AUTHENTICATION_EVENT,
#             function=do_something,
#             depends_on_exchange=common_settings.AUTHENTICATION_EVENT_EXCHANGE_NAME
#         )
#
#     async def init(self):
#         """
#         Метод инициализации всех очередей и обменников внутри контроллера для конкретного сервиса.
#         У каждого сервиса набор и названия очередей/обменников свой.
#         """
#         try:
#             """
#             пока так, т.к. не продумана логика явного ожидания поднятия сервиса, где объявляется обменник (обменника
#             может не быть, а очередь к нему подвязывается)
#             эта проблема может быть легко решена путем создания сущности обменника в самом контроллере с целью только
#             привязки очереди к обменнику, без использования контроллером обменника напрямую.
#             """
#             if not self.queue_for_listening_events_from_another_service:
#                 self.queue_for_listening_events_from_another_service = await self.rabbit.declare_queue(
#                     queue_name=self.queue_and_exchange_event_schema.queue,
#                     exchange_name=self.queue_and_exchange_event_schema.depends_on_exchange)
#         except Exception as e:
#             AppLogger.error(e.__str__())
#             await self.rabbit.reconnect_channel()
#
#         if not self.new_user_event_exchange:
#             self.new_user_event_exchange = await self.rabbit.declare_exchange(
#                 exchange_name=common_settings.NEW_USERS_EVENT_EXCHANGE_NAME
#             )
#
#     async def consume_queue_for_events_from_another_service(self) -> None:
#         """
#         Метод - пример как настроить прослушку с внешнего сервиса ивентов.
#         Очередь принадлежит этому сервису, а обменник общий, деклалирутеся очередь и ее связь с обменником.
#         На каждый ивент нужна своя очередь в контроллере потребителя и отдельный метод прослушивания.
#         """
#         await self.init()
#         await self.rabbit.consume_queue(
#             queue_instance=self.queue_for_listening_events_from_another_service,
#             do_something=self.queue_and_exchange_event_schema.function
#         )
#
#     async def publish_new_user_event(
#             self,
#             data_schema: BaseModel,
#             convert_data_type: Optional[Literal['json']] = None
#     ) -> None:
#         """
#         Метод публикации сообщения в обменник.
#         :param exchange_name: имя обменника.
#         :param data_schema: заполненные данные в виде схемы pydantic для отправки.
#         :param convert_data_type: тип конвертации данных.
#         :return: ничего.
#         """
#         async with self.rabbit.rabbitmq_async_connection:
#             if not self.new_user_event_exchange:
#                 await self.init()
#
#             to_send = data_schema
#             if convert_data_type:
#                 to_send = self.rabbit.convert_data_to_message_sending_type(data_schema, convert_data_type)
#             await self.new_user_event_exchange.publish(to_send, routing_key="info")

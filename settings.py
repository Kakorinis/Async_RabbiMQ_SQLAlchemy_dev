from core.settings import CoreSettings


class Settings(CoreSettings):

    # реббит
    RABBIT_LOGIN: str
    RABBIT_PASSWORD: str
    RABBIT_SERVICE_NAME: str
    RABBIT_PROTOCOL: str
    LOGGING_QUEUE_NAME: str
    QUEUE_FOR_OTHER_SERVICE_EVENT: str = ''
    OTHER_EVENT_EXCHANGE_NAME: str = ''
    USERS_EVENT_EXCHANGE_NAME: str = ''
    RABBIT_URL_: str = ''
    # MY_SERVICE_EXCHANGE_NAME: str
    # AUTHOR_SERVICE_QUEUE_NAME: str

    QUEUES_EXCHANGES_COMBINATIONS: list = [
        {
            'exchange': 'new_users',
            'queues_for_exchange': [
                'authent_queue',
            ]
        },
    ]

    @property
    def RABBIT_URL(self) -> str:
        if not self.RABBIT_URL_:
            self.RABBIT_URL_ = (f"{self.RABBIT_PROTOCOL}://{self.RABBIT_LOGIN}:{self.RABBIT_PASSWORD}@"
                                f"{self.RABBIT_SERVICE_NAME}/")
        return self.RABBIT_URL_


common_settings = Settings()

from authentication_service.settings import common_settings
from core.models import MixinAutoIdModel


class BaseDbModel(MixinAutoIdModel):
    """
    Базовая модель для ORM c автоинкрементным id.
    Используется для указания схемы.
    """

    __abstract__ = True
    __table_args__ = {
        'schema': common_settings.AUTH_SQL_SCHEMA,
    }

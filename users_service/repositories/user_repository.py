from sqlalchemy.orm import sessionmaker

from core.repositories import BaseRepository
from users_service.models import Users
from users_service.schemas.dtos import UserDtoWithId


class UserRepository(BaseRepository):
    """
    Репозиторий для работы с таблицей users.
    """
    def __init__(self, session_maker: sessionmaker):
        super().__init__(
            model=Users,
            session_maker=session_maker,
            with_id_dto=UserDtoWithId
        )

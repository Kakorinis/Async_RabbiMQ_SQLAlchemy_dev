from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from core.repositories import BaseRepository
from authentication_service.models import AuthUsers
from authentication_service.schemas.dtos import AuthUserDtoWithId


class AuthRepository(BaseRepository):
    """
    Репозиторий для работы с таблицей auth_users.
    """
    def __init__(self, session_maker: sessionmaker):
        super().__init__(
            model=AuthUsers,
            session_maker=session_maker,
            with_id_dto=AuthUserDtoWithId
        )

    async def get_one_by_user_id(self, user_id: int) -> AuthUserDtoWithId | None:
        stmt = select(AuthUsers).where(AuthUsers.user_id == user_id)
        with self.session_maker as session:
            model = await session.scalar(stmt)
            return AuthUserDtoWithId.model_validate(model) if model else None

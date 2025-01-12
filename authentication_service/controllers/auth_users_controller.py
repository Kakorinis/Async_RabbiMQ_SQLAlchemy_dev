from fastapi import HTTPException

from authentication_service.repositories import AuthRepository
from authentication_service.schemas.dtos import AuthUserDto, AuthUserDtoWithId
from core.logger import AppLogger
from .auth_rabbit_controller import AuthRabbitController


class AuthUserController:
    def __init__(
            self,
            main_repository: AuthRepository,
            rabbit: AuthRabbitController
    ):
        self.main_repository = main_repository
        self.rabbit = rabbit

    async def add_new_one(self, user: AuthUserDto) -> AuthUserDtoWithId:
        new_user = await self.main_repository.add_one(data_schema=user)

        await self.rabbit.publish_new_own_event(data_schema=new_user)  # , convert_data_type='json')
        AppLogger.info("В обменник отправлено сообщение о записи в БД хеш-пароля нового пользователя")
        return new_user

    async def get_one(self, id_: int) -> AuthUserDtoWithId:
        user = await self.main_repository.get_one_by_id(id_)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_one_by_user_id(self, id_: int) -> AuthUserDtoWithId:
        user = await self.main_repository.get_one_by_user_id(id_)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update(self, dto: AuthUserDtoWithId) -> AuthUserDtoWithId:
        return await self.main_repository.update_one(dto)

    async def delete_one(self, id_: int):
        return await self.main_repository.delete_one_by_id(id_)

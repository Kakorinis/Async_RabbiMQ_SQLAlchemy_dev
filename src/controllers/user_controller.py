from core.logger import AppLogger
from core.utils.common import make_hashed_pwd
from src.repositories import UserRepository
from src.schemas.dtos import UserDto, UserDtoWithId
from .rabbit_controller import RabbitController
from fastapi import HTTPException


class UserController:
    def __init__(
            self,
            main_repository: UserRepository,
            rabbit: RabbitController
    ):
        self.main_repository = main_repository
        self.rabbit = rabbit

    async def add_new_one(self, user: UserDto) -> UserDtoWithId:
        user.password = make_hashed_pwd(user.password)
        new_user = await self.main_repository.add_one(data_schema=user)

        await self.rabbit.publish_new_user_event(data_schema=new_user)  # , convert_data_type='json')
        AppLogger.info("В обменник отправлено сообщение о появлении нового пользователя с его данными")
        return new_user

    async def get_one(self, id_: int) -> UserDtoWithId:
        user = await self.main_repository.get_one_by_id(id_)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update(self, dto: UserDtoWithId) -> UserDtoWithId:
        return await self.main_repository.update_one(dto)

    async def delete_one(self, id_: int):
        return await self.main_repository.delete_one_by_id(id_)

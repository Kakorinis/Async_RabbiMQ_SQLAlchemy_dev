from core.logger import AppLogger
from core.utils.common import make_hashed_pwd
from users_service.repositories import UserRepository
from users_service.schemas.dtos import UserDto, UserDtoWithId, UserAuthDto
from .rabbit_controller import RabbitController
from fastapi import HTTPException

from users_service.schemas.dtos.user_base_dto import UserBaseDto


class UserController:
    def __init__(
            self,
            main_repository: UserRepository,
            rabbit: RabbitController
    ):
        self.main_repository = main_repository
        self.rabbit = rabbit

    async def add_new_one(self, user: UserDto) -> UserDtoWithId:
        new_user = await self.main_repository.add_one(data_schema=UserBaseDto.parse_obj(user))

        await self.rabbit.publish_new_own_event(
            data_schema=UserAuthDto(
                user_id=new_user.id,
                login=user.login,
                password=make_hashed_pwd(user.password)
            )
        )
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

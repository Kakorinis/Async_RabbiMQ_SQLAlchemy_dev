from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from core.logger import AppLogger
from core.schemas.responses import ErrorSchema
from src.controllers import UserController
from src.depends import UserServiceContainer
from src.schemas.dtos import UserDto
from src.schemas.dtos import UserDtoWithId

user_router = APIRouter()


@user_router.post(
    path="/add_one",
    summary='Добавление нового пользователя',
    response_model=UserDtoWithId,
    status_code=status.HTTP_200_OK
)
@inject
async def add_new_user(
        user: UserDto,
        user_controller: UserController = Depends(Provide[UserServiceContainer.user_controller]),  # Annotated[DBService, Provide[CommonContainer.db_service]] не работает check that typing.Annotated[core.controllers.db.db_manager.DBService is a valid Pydantic field typ
) -> UserDtoWithId:
    AppLogger.info(f"Регистрация нового пользователя: {user}")
    return await user_controller.add_new_one(user)


@user_router.post(
    path="/update",
    summary='Обновление данных о пользователе',
    response_model=UserDtoWithId,
    status_code=status.HTTP_200_OK
)
@inject
async def add_new_user(
        user: UserDtoWithId,
        user_controller: UserController = Depends(Provide[UserServiceContainer.user_controller]),  # Annotated[DBService, Provide[CommonContainer.db_service]] не работает check that typing.Annotated[core.controllers.db.db_manager.DBService is a valid Pydantic field typ
) -> UserDtoWithId:
    AppLogger.info(f"Обновление данных о пользователе: {user}")
    return await user_controller.update(user)


@user_router.get(
    path="/{id}",
    summary='Получение данных о пользователе',
    response_model=UserDtoWithId,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}}
)
@inject
async def get_one(
        id: int,
        user_controller: UserController = Depends(Provide[UserServiceContainer.user_controller]),  # Annotated[DBService, Provide[CommonContainer.db_service]] не работает check that typing.Annotated[core.controllers.db.db_manager.DBService is a valid Pydantic field typ
) -> UserDtoWithId:
    AppLogger.info(f"Получение данных о пользователе c id: {id}")
    return await user_controller.get_one(id)

@user_router.delete(
    path="/{id}",
    summary='Удаление пользователя',
    response_model=UserDtoWithId,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}}
)
@inject
async def delete_one(
        id: int,
        user_controller: UserController = Depends(Provide[UserServiceContainer.user_controller]),  # Annotated[DBService, Provide[CommonContainer.db_service]] не работает check that typing.Annotated[core.controllers.db.db_manager.DBService is a valid Pydantic field typ
) -> UserDtoWithId:
    AppLogger.info(f"Удаление пользователя c id: {id}")
    return await user_controller.delete_one(id)

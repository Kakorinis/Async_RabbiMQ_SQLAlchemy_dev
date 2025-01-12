from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from authentication_service.schemas.dtos import AuthUserDtoWithId
from core.logger import AppLogger
from core.schemas.responses import ErrorSchema
from authentication_service.controllers import AuthUserController
from authentication_service.depends import AuthServiceContainer
from users_service.schemas.dtos import UserDto
from users_service.schemas.dtos import UserDtoWithId

auth_router = APIRouter()


@auth_router.get(
    path="/{id}",
    summary='Получение данных о пользователе',
    response_model=AuthUserDtoWithId,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}}
)
@inject
async def get_one(
        id: int,
        auth_controller: AuthUserController = Depends(Provide[AuthServiceContainer.auth_controller]),
) -> AuthUserDtoWithId:
    AppLogger.info(f"Получение данных о пользователе c id: {id}")
    return await auth_controller.get_one(id)


@auth_router.get(
    path="/{user_id}",
    summary='Получение данных о пользователе по его user_id',
    response_model=AuthUserDtoWithId,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}}
)
@inject
async def get_one_by_user_id(
        user_id: int,
        auth_controller: AuthUserController = Depends(Provide[AuthServiceContainer.auth_controller]),  # Annotated[DBService, Provide[CommonContainer.db_service]] не работает check that typing.Annotated[core.controllers.db.db_manager.DBService is a valid Pydantic field typ
) -> AuthUserDtoWithId:
    AppLogger.info(f"Получение данных о пользователе c user_id: {user_id}")
    return await auth_controller.get_one_by_user_id(user_id)

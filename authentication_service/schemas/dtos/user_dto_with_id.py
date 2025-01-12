from core.schemas.dtos import MixinIdSchema
from .auth_user_dto import AuthUserDto


class AuthUserDtoWithId(MixinIdSchema, AuthUserDto):
    pass

from core.schemas.dtos import MixinIdSchema
from .user_dto import UserDto


class UserDtoWithId(MixinIdSchema, UserDto):
    pass

from core.schemas.dtos import MixinIdSchema
from .user_base_dto import UserBaseDto


class UserDtoWithId(MixinIdSchema, UserBaseDto):
    pass

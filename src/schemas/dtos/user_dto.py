from core.schemas.dtos import BaseSchema


class UserDto(BaseSchema):
    login: str
    password: str

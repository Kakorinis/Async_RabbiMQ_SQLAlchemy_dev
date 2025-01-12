from core.schemas.dtos import BaseSchema


class AuthUserDto(BaseSchema):
    user_id: str
    login: str
    password: str

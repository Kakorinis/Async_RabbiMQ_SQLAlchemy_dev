from core.schemas.dtos import BaseSchema


class UserMetadataDto(BaseSchema):
    login: str
    password: str

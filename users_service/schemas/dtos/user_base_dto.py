from core.schemas.dtos import BaseSchema


class UserBaseDto(BaseSchema):
    name: str = None
    surname: str = None
    middle_name: str = None
    office: str

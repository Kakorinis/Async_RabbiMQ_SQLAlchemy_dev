from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base_db_model import BaseDbModel


class Users(BaseDbModel):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    office: Mapped[str] = mapped_column(String, nullable=False)

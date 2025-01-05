from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_db_model import BaseDbModel


class Users(BaseDbModel):
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

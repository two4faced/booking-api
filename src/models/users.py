import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.database import Base


if typing.TYPE_CHECKING:
    from src.models import RatingsORM


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

    ratings: Mapped[list['RatingsORM']] = relationship(back_populates='user')

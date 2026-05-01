import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, CheckConstraint, VARCHAR, UniqueConstraint

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import UsersORM, HotelsORM


class RatingsORM(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id', ondelete='CASCADE'))
    rating: Mapped[int] = mapped_column(Integer, CheckConstraint('rating > 0 AND rating <= 5'))
    rating_text: Mapped[int] = mapped_column(VARCHAR(1000))

    __table_args__ = (UniqueConstraint('user_id', 'hotel_id', name='_user_hotel_ids_uc'),)

    user: Mapped['UsersORM'] = relationship(back_populates='ratings', lazy='selectin')
    hotel: Mapped['HotelsORM'] = relationship(back_populates='ratings', lazy='selectin')

import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, Float, ForeignKey, BIGINT

from src.database import Base


if typing.TYPE_CHECKING:
    from src.models import RoomsORM, RatingsORM, BookingsORM


class HotelsORM(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String)
    stars: Mapped[int]
    phone: Mapped[int] = mapped_column(BIGINT)
    rating: Mapped[float] = mapped_column(Float, default=0.0)

    rooms: Mapped[list['RoomsORM']] = relationship(
        back_populates='hotel', cascade='all, delete-orphan'
    )
    ratings: Mapped[list['RatingsORM']] = relationship(
        back_populates='hotel', cascade='all, delete-orphan'
    )
    bookings: Mapped[list['BookingsORM']] = relationship(
        back_populates='hotel', cascade='all, delete-orphan'
    )

    __table_args__ = (UniqueConstraint('title', 'location', name='_title_location_uc'),)

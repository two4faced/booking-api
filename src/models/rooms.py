import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import FacilitiesORM, HotelsORM


class RoomsORM(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey('hotels.id', ondelete='CASCADE')
    )
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    guests_count: Mapped[int]

    facilities: Mapped[list['FacilitiesORM']] = relationship(
        back_populates='rooms',
        secondary='room_facilities',
        lazy='selectin'
    )
    hotel: Mapped['HotelsORM'] = relationship(
        back_populates='rooms'
    )

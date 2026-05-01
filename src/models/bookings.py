import typing
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if typing.TYPE_CHECKING:
    from src.models import RoomsORM, HotelsORM


class BookingsORM(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id', ondelete='CASCADE'))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    hotel: Mapped['HotelsORM'] = relationship(back_populates='bookings')
    room: Mapped['RoomsORM'] = relationship()

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days

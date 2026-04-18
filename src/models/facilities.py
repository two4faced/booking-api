import typing

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsORM


class FacilitiesORM(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates='facilities',
        secondary='room_facilities',
        lazy='selectin'
    )


class RoomFacilitiesORM(Base):
    __tablename__ = 'room_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))

    __table_args__ = (UniqueConstraint('room_id', 'facility_id', name='uix_room_facility'),)

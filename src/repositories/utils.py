from datetime import date

from sqlalchemy import func, select, Select, Subquery

from src.models import RatingsORM
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
    guests_count: int | None = None,
) -> Select:
    rooms_count = (
        select(BookingsORM.room_id, func.count('*').label('rooms_booked'))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name='rooms_count')
    )

    rooms_left_table = (
        select(
            RoomsORM.id.label('room_id'),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left'),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name='rooms_left')
    )

    rooms_ids_for_hotel = select(RoomsORM.id).select_from(RoomsORM)

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    if guests_count is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter(RoomsORM.guests_count >= guests_count)

    rooms_ids_for_hotel_subquery: Subquery = rooms_ids_for_hotel.subquery(
        name='rooms_ids_for_hotel'
    )

    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel_subquery),  # type: ignore
        )
    )

    return rooms_ids_to_get


def get_average_rating(hotel_id: int):
    avg_rating = select(func.round(func.avg(RatingsORM.rating), 1)).where(
        RatingsORM.hotel_id == hotel_id
    )

    return avg_rating

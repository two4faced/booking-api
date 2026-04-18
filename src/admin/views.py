from sqladmin import ModelView

from src.models import *


class UsersAdmin(ModelView, model=UsersORM):
    name_plural = 'Users'
    column_list = [UsersORM.id, UsersORM.name, UsersORM.email, UsersORM.role]

    column_details_exclude_list = ['hashed_password']


class HotelsAdmin(ModelView, model=HotelsORM):
    name_plural = 'Hotels'

    column_list = [
        HotelsORM.id,
        HotelsORM.title,
        HotelsORM.location,
        HotelsORM.stars,
        HotelsORM.rating,
    ]


class RoomsAdmin(ModelView, model=RoomsORM):
    name_plural = 'Rooms'

    column_list = [
        RoomsORM.id,
        RoomsORM.hotel_id,
        RoomsORM.title,
        RoomsORM.description,
        RoomsORM.price,
        RoomsORM.quantity,
        RoomsORM.guests_count,
    ]


class BookingsAdmin(ModelView, model=BookingsORM):
    name_plural = 'Bookings'

    column_list = [
        BookingsORM.id,
        BookingsORM.user_id,
        BookingsORM.hotel_id,
        BookingsORM.room_id,
        BookingsORM.date_from,
        BookingsORM.date_to,
        BookingsORM.price,
    ]


class RatingsAdmin(ModelView, model=RatingsORM):
    name_plural = 'Ratings'

    column_list = [
        RatingsORM.id,
        RatingsORM.user_id,
        RatingsORM.hotel_id,
        RatingsORM.rating,
        RatingsORM.rating_text,
    ]


class FacilitiesAdmin(ModelView, model=FacilitiesORM):
    name_plural = 'Facilities'

    column_list = [FacilitiesORM.id, FacilitiesORM.title]

from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingsAddRequest(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BookingsAddRequest):
    user_id: int
    price: int


class Bookings(BookingsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

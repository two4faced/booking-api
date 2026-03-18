from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsBookedException,
    AllRoomsBookedHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    DateFromLaterThenOrEQDateToException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.bookings import BookingsAddRequest
from src.services.bookings import BookingsService

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('', summary='Получить все бронирования')
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get('/me', summary='Получить свои бронирования')
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await BookingsService(db).get_my_bookings(user_id)


@router.post('', summary='Забронировать номер')
async def book_room(user_id: UserIdDep, booking_data: BookingsAddRequest, db: DBDep):
    try:
        booking = await BookingsService(db).book_room(user_id, booking_data)
    except AllRoomsBookedException:
        raise AllRoomsBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except DateFromLaterThenOrEQDateToException as exc:
        raise HTTPException(status_code=400, detail=exc.detail)

    await db.commit()
    return {'status': 'OK', 'data': booking}

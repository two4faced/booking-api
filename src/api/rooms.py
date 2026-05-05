from datetime import date

from fastapi import Path, APIRouter, HTTPException, Query

from src.api.dependencies import DBDep, RequireOwnerDep, RequireAdminDep
from src.exceptions import (
    DateFromLaterThenOrEQDateToException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
    ObjectNotFoundException,
    FacilitiesNotFoundHTTTPException,
    NothingChangedException,
    NothingChangedHTTPException,
    ObjectBookedException,
    RoomBookedHTTPException,
)
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest
from src.services.bookings import BookingsService
from src.services.rooms import RoomsService

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms', summary='Получить номера отеля')
async def get_rooms(
    db: DBDep,
    date_from: date = Query(example='2024-08-01', description='Дата заезда'),
    date_to: date = Query(example='2024-08-10', description='Дата выезда'),
    hotel_id: int = Path(),
):
    try:
        return await RoomsService(db).get_rooms(date_from, date_to, hotel_id)
    except DateFromLaterThenOrEQDateToException as exc:
        raise HTTPException(status_code=400, detail=exc.detail)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получить номер')
async def get_room(
    db: DBDep,
    room_id: int = Path(description='ID номера'),
    hotel_id: int = Path(description='ID отеля'),
):
    try:
        result = await RoomsService(db).get_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return result


@router.post('/{hotel_id}/rooms', summary='Добавить номер', dependencies=[RequireOwnerDep])
async def add_room(room_data: RoomsAddRequest, db: DBDep, hotel_id: int = Path()):
    try:
        result = await RoomsService(db).add_room(room_data, hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except ObjectNotFoundException:
        raise FacilitiesNotFoundHTTTPException

    return {'status': 'OK', 'data': result}


@router.delete(
    '/{hotel_id}/rooms/{room_id}', summary='Удалить номер', dependencies=[RequireAdminDep]
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await BookingsService(db).check_room_bookings(room_id=room_id)
        await RoomsService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except ObjectBookedException:
        raise RoomBookedHTTPException

    return {'status': 'OK'}


@router.patch(
    '/{hotel_id}/rooms/{room_id}', summary='Частично изменить номер', dependencies=[RequireOwnerDep]
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsPatchRequest):
    try:
        await RoomsService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NothingChangedException:
        raise NothingChangedHTTPException

    return {'status': 'OK'}


@router.put('/{hotel_id}/rooms/{room_id}', summary='Изменить номер', dependencies=[RequireOwnerDep])
async def change_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest, db: DBDep):
    try:
        await RoomsService(db).change_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except ObjectNotFoundException:
        raise FacilitiesNotFoundHTTTPException
    return {'status': 'OK'}

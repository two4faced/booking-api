from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep, RequireAdminDep
from src.exceptions import (
    ObjectNotFoundException,
    DateFromLaterThenOrEQDateToException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    NothingChangedException,
    NothingChangedHTTPException,
    ObjectBookedException,
    HotelBookedHTTPException,
)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.bookings import BookingsService
from src.services.hotels import HotelsService

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('', summary='Получить отели')
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Локация отеля'),
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10'),
    guests_count: int | None = Query(
    None,
    description='Количество гостей')
):
    try:
        hotels = await HotelsService(db).get_hotels(pagination, title, location, date_from, date_to, guests_count)
    except DateFromLaterThenOrEQDateToException as exc:
        raise HTTPException(status_code=400, detail=exc.detail)

    return {'hotels': hotels}


@router.get('/{hotel_id}', summary='Получить один отель')
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post('', summary='Добавить отель')
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {
                    'title': 'Отель 5 звезд у моря',
                    'location': 'г. Сочи, ул. Моря, 1',
                    'stars': 3,
                },
            },
            '2': {
                'summary': 'Дубай',
                'value': {
                    'title': 'Отель У фонтана',
                    'location': 'Дубай, ул. Шейха, 2',
                    'stars': 5,
                },
            },
        }
    ),
):
    result = await HotelsService(db).create_hotel(hotel_data)
    return {'status': 'OK', 'data': result}


@router.delete('/{hotel_id}', summary='Удалить отель', dependencies=[RequireAdminDep])
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await BookingsService(db).check_bookings(hotel_id=hotel_id)
        await HotelsService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except ObjectBookedException:
        raise HotelBookedHTTPException
    return {'status': 'OK'}


@router.put('/{hotel_id}', summary='Изменить отель')
async def change_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelsService(db).change_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {'status': 'OK'}


@router.patch('/{hotel_id}', summary='Частично изменить отель')
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        await HotelsService(db).patch_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except NothingChangedException:
        raise NothingChangedHTTPException
    return {'status': 'OK'}

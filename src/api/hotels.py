from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import (
    PaginationDep,
    DBDep,
    RequireAdminDep,
    RequireOwnerDep,
    UserIdDep,
)
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
from src.schemas.hotels import HotelPatch, HotelAdd, RequestHotelAdd
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
    guests_count: int | None = Query(None, description='Количество гостей'),
    min_price: int | None = Query(None, description='Минимальная цена'),
    max_price: int | None = Query(None, description='Максимальная цена'),
    sort_by: str | None = Query(
        'price_asc', description='price_asc / price_desc / rating_desc / rating_asc'
    ),
):
    try:
        hotels = await HotelsService(db).get_hotels(
            pagination=pagination,
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            guests_count=guests_count,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
        )
    except DateFromLaterThenOrEQDateToException as exc:
        raise HTTPException(status_code=400, detail=exc.detail)

    return {'hotels': hotels}


@router.get('/{hotel_id}', summary='Получить один отель')
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post('', summary='Добавить отель', dependencies=[RequireOwnerDep])
async def create_hotel(
    user_id: UserIdDep,
    db: DBDep,
    hotel_data: RequestHotelAdd = Body(
        openapi_examples={
            '1': {
                'summary': 'Сочи',
                'value': {
                    'title': 'Отель 5 звезд у моря',
                    'location': 'г. Сочи, ул. Моря, 1',
                    'stars': 3,
                    'phone': 8189874656,
                },
            },
            '2': {
                'summary': 'Дубай',
                'value': {
                    'title': 'Отель У фонтана',
                    'location': 'Дубай, ул. Шейха, 2',
                    'stars': 5,
                    'phone': 79457682324,
                },
            },
        }
    ),
):
    new_hotel_data = HotelAdd(owner_id=user_id, **hotel_data.model_dump())
    result = await HotelsService(db).create_hotel(new_hotel_data)
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


@router.patch('/{hotel_id}', summary='Частично изменить отель', dependencies=[RequireOwnerDep])
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        await HotelsService(db).patch_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except NothingChangedException:
        raise NothingChangedHTTPException
    return {'status': 'OK'}

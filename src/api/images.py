from fastapi import APIRouter, UploadFile

from src.api.dependencies import DBDep
from src.exceptions import (
    WrongExtensionException,
    WrongExtensionHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.services.hotels import HotelsService
from src.services.images import ImagesService
from src.services.rooms import RoomsService

router = APIRouter(prefix='', tags=['Изображения'])


@router.post('/hotels/{hotel_id}/images')
async def add_hotel_image(file: UploadFile, hotel_id: int, db: DBDep):
    try:
        await HotelsService(db).check_hotel_existence(hotel_id=hotel_id)
        await ImagesService(db).add_hotel_image(file, hotel_id)
    except WrongExtensionException:
        raise WrongExtensionHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {'status': 'OK'}


@router.get('/hotels/{hotel_id}/images')
async def get_all_hotel_images(hotel_id: int, db: DBDep):
    try:
        await HotelsService(db).check_hotel_existence(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return await ImagesService(db).get_all_hotel_images(hotel_id=hotel_id)


@router.post('/hotels/{hotel_id}/rooms/{room_id}/images')
async def add_room_image(file: UploadFile, hotel_id: int, room_id: int, db: DBDep):
    try:
        await HotelsService(db).check_hotel_existence(hotel_id)
        await RoomsService(db).check_room_existence(room_id)

        await ImagesService(db).add_room_image(file, hotel_id, room_id)
    except WrongExtensionException:
        raise WrongExtensionHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {'status': 'OK'}


@router.get('/hotels/{hotel_id}/rooms/{room_id}/images')
async def get_all_room_images(hotel_id: int, room_id: int, db: DBDep):
    try:
        await HotelsService(db).check_hotel_existence(hotel_id)
        await RoomsService(db).check_room_existence(room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return await ImagesService(db).get_all_room_images(room_id=room_id)

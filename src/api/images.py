from fastapi import APIRouter, UploadFile

from src.api.dependencies import DBDep
from src.services.images import ImagesService

router = APIRouter(prefix='', tags=['Изображения'])


@router.post('/hotels/{hotel_id}/images')
async def add_hotel_image(file: UploadFile, hotel_id: int, db: DBDep):
    await ImagesService(db).add_hotel_image(file, hotel_id)
    return {'status': 'OK'}


@router.get('/hotels/{hotel_id}/images')
async def get_all_hotel_images(hotel_id: int, db: DBDep):
    return await ImagesService(db).get_all_hotel_images(hotel_id=hotel_id)


@router.post('/hotels/{hotel_id}/rooms/{room_id}/images')
async def add_room_image(file: UploadFile, hotel_id: int, room_id: int, db: DBDep):
    await ImagesService(db).add_room_image(file, hotel_id, room_id)
    return {'status': 'OK'}


@router.get('/hotels/{hotel_id}/rooms/{room_id}/images')
async def get_all_room_images(room_id: int, db: DBDep):
    return await ImagesService(db).get_all_room_images(room_id=room_id)

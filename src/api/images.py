from fastapi import APIRouter, UploadFile

from src.api.dependencies import DBDep
from src.services.images import ImagesService

router = APIRouter(prefix='', tags=['Изображения'])


@router.post('/hotels/{hotel_id}/images')
async def add_hotel_image(file: UploadFile, hotel_id: int, db: DBDep):
    await ImagesService(db).add_hotel_image(file, hotel_id)
    return {'status': 'OK'}


@router.post('/hotels/{hotel_id}/rooms/{room_id}/images')
def add_room_image(file: UploadFile, hotel_id: int, room_id: int):
    image_path = ImagesService().add_room_image(file, hotel_id, room_id)

    return {'status': 'OK', 'path': image_path}

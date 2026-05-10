import os
import shutil
from pathlib import Path

from fastapi import UploadFile

from src.schemas.images import HotelImageAdd
from src.services.base import BaseService


class ImagesService(BaseService):
    async def add_hotel_image(self, file: UploadFile, hotel_id: int):
        directory = Path(f'src/static/images/{hotel_id}')
        directory.mkdir(parents=True, exist_ok=True)
        image_path = directory / file.filename

        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        new_image = HotelImageAdd(hotel_id=hotel_id, path=str(image_path))
        await self.db.hotels_images.add(new_image)
        await self.db.commit()

    def add_room_image(self, file: UploadFile, hotel_id: int, room_id: int):
        directory = Path(f'src/static/images/{hotel_id}/{room_id}')
        os.makedirs(directory, exist_ok=True)
        image_path = f'{directory}/{file.filename}'

        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(file.file, new_file)

        return image_path
